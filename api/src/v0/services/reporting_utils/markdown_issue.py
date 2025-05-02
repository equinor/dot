"""
Module for converting the issue data into markdown
"""
from .markdown_elements import header, unordered_list


categories = ["Fact", "Decision", "Uncertainty", "Value Metric", "Action Item", "Uncategorized"]
boundaries = ["in", "on", "out", "Unset"]
decisions = ["Policy", "Focus", "Tactical", "Unset"]
uncertainties = ["true", "false", "Unset"]



def group_issues(data: list[dict]) -> list[dict]:
    data_ = [{k:v if k != "category" or v else "Uncategorized" for k,v in item.items()} for item in data]
    data_ = [{k:v if k != "boundary" or v else "Unset" for k,v in item.items()} for item in data_]
    data_ = [{k:v if k != "decisionType" or v else "Unset" for k,v in item.items()} for item in data_]
    data_ = [{k:v if k != "keyUncertainty" or v else "Unset" for k,v in item.items()} for item in data_]
    data_.sort(key=lambda x: (
        categories.index(x["category"]),
        boundaries.index(x["boundary"]),
        decisions.index(x["decisionType"]),
        uncertainties.index(x["keyUncertainty"])
        )
        )
    return data_


def clean_issues(data: list[dict], category: str, keys: list[str]) -> list[dict]:
    d = [item for item in data if item["category"] == category]
    d = [{k:item[k] for k in keys if k in item.keys() and item[k] != "Unset"}
         for item in d]
    return d


def add_facts(data: list[dict], level=1) -> str:
    keys = ["description", "boundary", "shortname"]
    d = clean_issues(data, "Fact", keys)
    md = ""
    if d:
        md += header(level=level+2, prefix="Facts")
        md += unordered_list(d)
    return md


def add_action_item(data: list[dict], level=1) -> str:
    keys = ["description", "boundary", "shortname"]
    d = clean_issues(data, "Action Item", keys)
    md = ""
    if d:
        md += header(level=level+2, prefix="Action items")
        md += unordered_list(d)
    return md


def add_value_metric(data: list[dict], level=1) -> str:
    keys = ["description", "boundary", "shortname"]
    d = clean_issues(data, "Value Metric", keys)
    md = ""
    if d:
        md += header(level=level+2, prefix="Value metrics")
        md += unordered_list(d)
    return md


def add_uncategorized(data: list[dict], level=1) -> str:
    keys = ["description", "boundary", "shortname"]
    d = clean_issues(data, "Uncategorized", keys)
    md = ""
    if d:
        md += header(level=level+2, prefix="Uncategorized")
        md += unordered_list(d)
    return md


def add_decision(data: list[dict], level=1) -> str:
    keys = ["description", "boundary", "shortname", "decisionType", "alternatives"]
    d = clean_issues(data, "Decision", keys)
    md = ""
    if d:
        md += header(level=level+2, prefix="Decisions")
        md += unordered_list(d)
    return md


def generate_issue_data(data: list[dict], level=1) -> str:
    """generate the issue data in markdown format

    Args:
        data (list): issue data from database
        level (int, optional): level of markdown section. Defaults to 1.

    Returns:
        str: a markdown representation of the issue data
    """
    grouped_data = group_issues(data)