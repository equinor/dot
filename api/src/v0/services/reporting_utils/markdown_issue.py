"""
Module for converting the issue data into markdown
"""

from .markdown_elements import header, multitype_list

categories = [
    "Fact",
    "Decision",
    "Uncertainty",
    "Value Metric",
    "Action Item",
    "Uncategorized",
]
boundaries = ["in", "on", "out", "Unset"]
decisions = ["Policy", "Focus", "Tactical", "Unset"]
uncertainties = ["true", "false", "Unset"]


def group_issues(data: list[dict]) -> list[dict]:
    """Group data by category and sort them by category, boundary, decisionType and
    keyUncertainty


    Args:
        data (list[dict]): issues list

    Returns:
        list[dict]: a grouped and sorted issue list
    """
    data_ = [{k: v if v != "None" else None for k, v in item.items()} for item in data]
    data_ = [
        {k: v if k != "category" or v else "Uncategorized" for k, v in item.items()}
        for item in data_
    ]
    data_ = [
        {k: v if k != "boundary" or v else "Unset" for k, v in item.items()}
        for item in data_
    ]
    data_ = [
        {k: v if k != "decisionType" or v else "Unset" for k, v in item.items()}
        for item in data_
    ]
    data_ = [
        {k: v if k != "keyUncertainty" or v else "Unset" for k, v in item.items()}
        for item in data_
    ]
    data_.sort(
        key=lambda x: (
            categories.index(x["category"]),
            boundaries.index(x["boundary"]),
            decisions.index(x["decisionType"]),
            uncertainties.index(x["keyUncertainty"]),
        )
    )

    return data_


def clean_issues(data: list[dict], category: str, keys: list[str]) -> list[dict]:
    """clean data for each category.

        The cleaning consists of keeping data for only one category and within
        this category, keeping only desired attributes having values

    Args:
        data (list[dict]): list of issues
        category (str): category to clean
        keys (list[str]): list of keys (attributes) to keep in the output

    Returns:
        list[dict]: subset of the input list of issues
    """
    d = [item for item in data if item["category"] == category]
    d = [
        {k: item[k] for k in keys if k in item.keys() and item[k] != "Unset" and item[k]}
        for item in d
    ]
    return d


def keyword_translation(d: list[dict], translation: dict) -> list[dict]:
    """rename keywords of a dictionary

    Args:
        d (list[dict]): input data 
        translation (dict): mapping of the keywords

    Returns:
        list[dict]: data for which some keys have been renamed
    """
    return [
        {k if k not in translation else translation[k]: v for k, v in item.items()}
        for item in d
    ]


def add_facts(data: list[dict], level=1) -> str:
    """add facts to report

    Args:
        data (list[dict]): list of facts
        level (int, optional): level of main section. Defaults to 1.

    Returns:
        str: a markdown section listing facts
    """
    keys = ["description", "boundary", "shortname"]
    d = clean_issues(data, "Fact", keys)
    md = ""
    if d:
        md += header(level=level + 2, prefix="Facts")
        md += multitype_list(d)
    return md


def add_action_item(data: list[dict], level=1) -> str:
    """add action items to report

    Args:
        data (list[dict]): list of facts
        level (int, optional): level of main section. Defaults to 1.

    Returns:
        str: a markdown section listing action items
    """
    keys = ["description", "boundary", "shortname"]
    d = clean_issues(data, "Action Item", keys)
    md = ""
    if d:
        md += header(level=level + 2, prefix="Action items")
        md += multitype_list(d)
    return md


def add_value_metric(data: list[dict], level=1) -> str:
    """add Value metrics to report

    Args:
        data (list[dict]): list of facts
        level (int, optional): level of main section. Defaults to 1.

    Returns:
        str: a markdown section listing Value metrics
    """
    keys = ["description", "boundary", "shortname"]
    d = clean_issues(data, "Value Metric", keys)
    md = ""
    if d:
        md += header(level=level + 2, prefix="Value metrics")
        md += multitype_list(d)
    return md


def add_uncategorized(data: list[dict], level=1) -> str:
    """add uncategorized items to report

    Args:
        data (list[dict]): list of facts
        level (int, optional): level of main section. Defaults to 1.

    Returns:
        str: a markdown section listing uncategorized items
    """
    keys = ["description", "boundary", "shortname"]
    d = clean_issues(data, "Uncategorized", keys)
    md = ""
    if d:
        md += header(level=level + 2, prefix="Uncategorized")
        md += multitype_list(d)
    return md


def add_decision(data: list[dict], level=1) -> str:
    """add decisions to report

    Args:
        data (list[dict]): list of facts
        level (int, optional): level of main section. Defaults to 1.

    Returns:
        str: a markdown section listing decisions
    """
    keys = ["description", "boundary", "shortname", "decisionType", "alternatives"]
    d = clean_issues(data, "Decision", keys)
    translation = {"decisionType": "decision type"}
    d = keyword_translation(d, translation)
    md = ""
    if d:
        md += header(level=level + 2, prefix="Decisions")
        md += multitype_list(d)
    return md


def add_uncertainty(data: list[dict], level=1) -> str:
    """add uncertainties to report

    Args:
        data (list[dict]): list of facts
        level (int, optional): level of main section. Defaults to 1.

    Returns:
        str: a markdown section listing uncertainties
    """
    keys = ["description", "boundary", "shortname", "keyUncertainty", "probabilities"]
    d = clean_issues(data, "Uncertainty", keys)
    translation = {"keyUncertainty": "key uncertainty"}
    d = keyword_translation(d, translation)
    md = ""
    if d:
        md += header(level=level + 2, prefix="Uncertainties")
        md += multitype_list(d)
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
    md = ""
    md += header(level=level + 1, prefix="List of issues")
    md += add_value_metric(grouped_data, level)
    md += add_decision(grouped_data, level)
    md += add_uncertainty(grouped_data, level)
    md += add_facts(grouped_data, level)
    md += add_action_item(grouped_data, level)
    md += add_uncategorized(grouped_data, level)
    return md
