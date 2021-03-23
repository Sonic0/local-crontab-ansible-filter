Status: _IN PROGRESS_

# local-crontab-ansible-filter
Ansible filter with a few tools to handle with crontab string.
Those tools are:
- aws_standard_cron
- standard_aws_cron
- aws_local_aws_utc_crons
- standard_local_utc_crons
  
TODO (maybe ლ(╥﹏╥ლ))
- Convert localized cron to single UTC. Standard and AWS.

Probably the filter will be only compatible with Python3.8 runtime due to dependecies.

## Test filters
Look at the ansible playbook in the root project and run it!
I have made my tests with _Ansible 2.9_.
```bash
ansible-playbook filter-examples.yaml
```
