"""
util
====

Contains utility classes/methods
"""


def get_issue_blocks(issue, link_types=['Blocked'], raise_fail=True):
    """ Returns an tuple of blocking and blocked issues
    """
    blocks = []
    blocked_by = []

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

    return (blocks, blocked_by)
