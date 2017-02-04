"""
util
====

Contains utility classes/methods
"""
import logging


ISSUE_STATUS_COLORS = {
    'in progress': '#bcebff',
    'new': '#bcffd0',
    'closed': '#ffd0bc',
    '_DEFAULT_': '#ffbceb',
}
"""Define fill colors for issues based on status"""

log = logging.getLogger(__name__)
"""Define a named logger"""


def get_issue_blocks(issue, link_types=['Blocked'], raise_fail=True):
    """ Returns an tuple of blocking and blocked issues
    """
    log.debug("get_issue_blocks({i}, [{links}])".format(
        i=issue.key,
        links=", ".join(link_types)))

    blocks = []
    blocked_by = []

    if not hasattr(issue.fields, 'issuelinks'):
        # This object was merely a reference and we must query the Jira
        # API to get the rest of it's data
        log.debug("get_issue_blocks({i}): Updating issue".format(i=issue.key))
        issue.update()

    for linked_issue in issue.fields.issuelinks:
        if linked_issue.type.name not in link_types:
            # Irrelevant issue link type
            continue

        if hasattr(linked_issue, 'outwardIssue'):
            blocks.append(linked_issue.outwardIssue)

        elif hasattr(linked_issue, 'inwardIssue'):
            blocked_by.append(linked_issue.inwardIssue)

        else:
            # Unknown issue link direction
            if raise_fail:
                raise NotImplementedError(
                        "Could not determine linkage direction")

    log.debug("get_issue_blocks({i}): Found {c}".format(
        i=issue.key,
        c=len(blocks + blocked_by)))
    return (blocks, blocked_by)


def get_issue_color(issue, default_color='_DEFAULT_'):
    """ Returns a hex code for an issue's color based on status
    """
    status = issue.fields.status.name.lower()
    if status in ISSUE_STATUS_COLORS:
        return ISSUE_STATUS_COLORS[status]

    # No color for status defined, send default
    return ISSUE_STATUS_COLORS[default_color]


def get_issue_styling(issue, *args, **kwargs):
    """ Returns a diict of additional keys for a node
    """
    styles = {}

    # Add the label
    styles.update({
        'label': "\n".join([
            issue.key,
            '(' + issue.fields.status.name + ')',
        ])
    })
    # Add background color
    styles.update({
        'style': 'filled',
        'fillcolor': get_issue_color(issue, *args, **kwargs)
    })

    return styles
