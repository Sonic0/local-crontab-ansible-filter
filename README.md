# local-crontab-ansible-filter
Ansible filter with a few tools to handle with crontab string.
Those tools are:
- aws_standard_cron
- standard_aws_cron
- aws_local_aws_utc_crons
- standard_local_utc_crons

Probably the filter will be only compatible with Python3.8 runtime due to dependecies.

## Some Examples
1. aws_local_aws_utc_crons:
    ```bash
    '39 05 * * ? *' | aws_local_aws_utc_crons('Europe/Rome')
    ```
    ```bash
    # result:
    [
        "39 4 * 1-2 * *",
        "39 4 1-27 3 ? *",
        "39 3 28-31 3 ? *",
        "39 3 * 4-9 * *",
        "39 3 1-30 10 ? *",
        "39 4 31 10 ? *",
        "39 4 * 11-12 * *"
    ]
    ```
2. standard_to_aws_cron
    1.  Add current year:
        ```bash
        '10 10 * 10 2' | standard_aws_cron
        ```
        ```bash
        '10 10 * 10 2 2021' # result
        ```
    2. Add year and convert '*' in '?' in the right position, from _aws_specific_details_ structure:
       ```bash
       aws_specific_details:
          year: 2022
          question_parts: [ 'day' ] # minute, hours, day, etc..
       ```
       ```bash
       '10 10 * 10 2' | standard_aws_cron(aws_specific_details)
       ```
       ```bash
       '10 10 ? 10 2 2022' # result
       ```

More examples in **filter-example.yaml** file.

## Test filters
Look at the ansible playbook in the root project and run it!
I have made my tests with _Ansible 2.9_.
```bash
ansible-playbook filter-examples.yaml
```

## Other info
This repo is part of my Cron-Converter projects group.
Its related repositories:
- [cron-converter](https://github.com/Sonic0/cron-converter)
- [local-crontab](https://github.com/Sonic0/local-crontab)
- [local-crontab-serverless-infrastructure](https://github.com/Sonic0/local-crontab-serverless-infrastructure)
- [local-crontab-web-converter](https://github.com/Sonic0/local-crontab-web-converter)
