Status: _IN PROGRESS_

# local-crontab-ansible-filter
Ansible filter with a few tools to handle with crontab string.
Those tools are:
- standard_to_aws_cron
- aws_to_standard_cron
- aws_local_aws_utc_crons
  
TODO (maybe ლ(╥﹏╥ლ))
- Convert localized cron to UTC list of cron. Standard.
- Convert localized cron to UTC. Standard and AWS.
- Convert UTC cron to localized.

Probably the filter will be only compatible with Python3.8 runtime due to dependecies.

## Test filters
Look at the ansible playbook in the root project and run it!
I have made my tests with _Ansible 2.9_.
```bash
ansible-playbook filter-examples.yaml
```
