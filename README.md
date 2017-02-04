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
