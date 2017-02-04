"""
util
====

Contains utility classes/methods
"""
import logging
import networkx as nx
from jira.exceptions import JIRAError


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
        try:
            issue.update()
        except JIRAError as e:
            if e.status_code == 400 \
                    and "You do not have permission" in e.text:
                # Current user does not have permission within the project
                # that this issue lives, ignore & return
                return ([], [])
            else:
                raise

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


def get_issue_graph(issue, graph=None, *args, **kwargs):
    """ Recursively generates an issue graph
    """
    if graph is None:
        # This is the initial issue
        log.debug("get_issue_blocks({i}): Instantiating new directed graph")
        graph = nx.DiGraph()

    # Add the node if it's not present
    if issue.key not in graph:
        log.debug("get_issue_blocks: Adding {}".format(issue.key))
        graph.add_node(issue.key,
                       **get_issue_styling(issue))

    # Enumerate blocked & blockers
    blocks, blockers = get_issue_blocks(issue)

    for b in blocks:
        log.info("get_issue_blocks: {i} <- {b}".format(
            i=issue.key,
            b=b.key))
    for b in blockers:
        log.info("get_issue_blocks: {i} -> {b}".format(
            i=issue.key,
            b=b.key))

    # Add the blocker nodes & recursive into them if they had
    # not yet been added
    for b in blocks + blockers:
        if b.key not in graph:
            # This issue is being seen for the first time, recurse
            # into the issue to find additional blockers.
            log.debug("Recursing into issue: {}".format(b.key))
            get_issue_graph(b, graph, *args, **kwargs)

    # Create the edges
    log.debug("get_issue_blocks: Adding edges for {i}".format(i=issue.key))
    for b in blocks:
        graph.add_edge(b.key, issue.key)
    for b in blockers:
        graph.add_edge(issue.key, b.key)

    # Return the graph
    return graph
