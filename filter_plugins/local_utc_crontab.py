# Copyright (c) 2021 Andrea Salvatori
# MIT License (see COPYING or https://opensource.org/licenses/MIT)

# This Filter aims to convert an localized AWS CloudWatch crontab to a standard crontab.
#
#  Main differences, with classic crontab, are:
#    * A year field
#    * ? instead of * sometimes
#    * Some others.. implementation TBD
#
# The data that is removed is returned as well so that it can be used to
# roundtrip back to an AWS CloudWatch crontab
from __future__ import (absolute_import, division, print_function)

from typing import TypedDict, List, Literal

__metaclass__ = type

from local_crontab import Converter
from local_crontab.converter import WrongTimezoneError
from ansible.errors import AnsibleFilterError, AnsibleError
from ansible.utils import helpers
from ansible.module_utils.six import string_types

cron_part_index_tuple = ('minute', 'hour', 'day', 'month', 'weekday', 'year')


class AwsSpecificDetails(TypedDict):
    year: str
    question_parts: List[Literal['minute', 'hour', 'day', 'month', 'weekday', 'year']]


class ConvertedCronFromAws(TypedDict):
    crontab: str
    aws_specific_details: AwsSpecificDetails


def aws_to_standard_cron(aws_cron_string: str) -> ConvertedCronFromAws:
    """
    Convert an AWS crontab to standard crontab. It just removes the year cron part and it translates '*' to '?'
    :param aws_cron_string: (str) AWS crontab string (https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html)
    :return: (ConvertedCronFromAws): dict with converted crontab and info to revert the process
    :raise: AnsibleFilterError: wrong input crontab string
    """
    if not isinstance(aws_cron_string, string_types):
        raise AnsibleFilterError('Invalid Ansible cron string')
    crontab_parts = aws_cron_string.strip().split()
    if len(crontab_parts) != 6:
        raise AnsibleFilterError(f"len: {len(crontab_parts)}. Invalid cron string format, this is not an AWS cron "
                                 f"(len 6)")
    # standard crontabs don't have a year
    crontab_year_part = crontab_parts.pop()
    # replace ? with *, but remember where they were
    question_parts = []
    for part in crontab_parts:
        if part == "?":
            # question_parts.append(part)
            question_part_index = crontab_parts.index(part)
            question_parts.append(cron_part_index_tuple[question_part_index])
            crontab_parts[question_part_index] = "*"

    return {"crontab": " ".join(crontab_parts),
            "aws_specific_details": {
                "year": crontab_year_part,
                "question_parts": question_parts
                }
            }


def standard_to_aws_cron(cron_string: str, aws_specific_details: AwsSpecificDetails) -> str:
    """
    Convert an standard crontab to AWS crontab. It just adds the year cron part and it translates '*' to '?',
    from aws_specific_details dict
    :param cron_string: (str) crontab string (https://en.wikipedia.org/wiki/Cron)
    :param aws_specific_details: (AwsSpecificDetails)
    :return: (str) AWS crontab string (https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html)
    """
    if not isinstance(cron_string, string_types):
        raise AnsibleFilterError('Invalid Ansible cron string')
    crontab_parts = cron_string.strip().split()
    if len(crontab_parts) != 5:
        raise AnsibleFilterError(f"len: {len(crontab_parts)}. Invalid cron string format")
    # replace * with ?
    for part in crontab_parts:
        if part == '*':
            asterisk_part_index = crontab_parts.index(part)  # What is the '*' index?
            question_part_index = cron_part_index_tuple[asterisk_part_index]  # What the corresponding cron part unit?
            if question_part_index in aws_specific_details["question_parts"]:  # Is the part unit in the list of replacebles?
                crontab_parts[asterisk_part_index] = crontab_parts[asterisk_part_index].replace("*", "?")
    # Append specified year as cron part
    crontab_parts.append(str(aws_specific_details["year"]))
    return " ".join(crontab_parts)


def aws_local_cron_to_aws_utc_crons(local_crontab: str, timezone: str) -> List[str]:
    """
    Convert a crontab, in a local timezone, into a set of UTC crontabs.
    It creates multiple UTC crontabs because of Daylight Saving Time.
    More info at https://github.com/Sonic0/local-crontab
    :param local_crontab: (str) AWS crontab string (https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html)
    :param timezone: (str) time zone as TZ database name (https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
    :return: List of UTC crontab strings
    """
    standard_cron: ConvertedCronFromAws = aws_to_standard_cron(local_crontab)
    try:
        utc_crontabs = Converter(standard_cron.get('crontab'), timezone).to_utc_crons()
    except WrongTimezoneError as ex:
        raise AnsibleFilterError(ex)
    except Exception as ex:
        raise AnsibleFilterError(ex)
    utc_crontabs = [standard_to_aws_cron(utc_crontab, standard_cron.get('aws_specific_details')) for utc_crontab in utc_crontabs]
    return utc_crontabs


# ---- Ansible filters ----
class FilterModule(object):
    """ Crontab filters """

    def filters(self):
        return {
            'aws_to_standard_cron': aws_to_standard_cron,
            'standard_to_aws_cron': standard_to_aws_cron,
            'aws_local_aws_utc_crons': aws_local_cron_to_aws_utc_crons
        }
