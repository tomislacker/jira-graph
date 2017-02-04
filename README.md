# JIRA Issue Grapher

## About
Assists is visualizing what JIRA issues are blocking each other.

## Usage
### Configuration
Create a `config.py` file that looks like this:

```python
JIRA_OPTS = {
    'server': 'https://jira.mydomain.com',
}

# HTTP Basic Auth
# NOTE: If your JIRA system uses SSO or similar authentication mechanisms, it
# will be necessary to set a local password within JIRA for your account.
JIRA_AUTH = ('<username>', '<password>')
```

## References
### Jira
- https://jira.readthedocs.io/en/master/examples.html#searching
- https://confluence.atlassian.com/jirakb/creating-issues-via-direct-html-links-159474.html
- https://answers.atlassian.com/questions/199842/function-in-jql-for-current-sprint
