"""
Module for converting the objective data into markdown
"""

from .markdown_elements import header, unordered_list


def group_objectives(data: list) -> dict:
    """Group objectives by category

    Args:
        data (list): opportunity data from database

    Returns:
        dict: objectives grouped by category.
    """
    grouped = {
        "Strategic": [item for item in data if item["hierarchy"] == "Strategic"],
        "Fundamental": [item for item in data if item["hierarchy"] == "Fundamental"],
        "Mean": [item for item in data if item["hierarchy"] == "Mean"],
        "Uncategorized": [
            item
            for item in data
            if item["hierarchy"] not in ["Strategic", "Fundamental", "Mean"]
        ],
    }
    return grouped


def add_objectives(data: dict, category: str, level=1) -> str:
    """add objectives by category to markdown

    Args:
        data (dict): objectives grouped by category
        category (str): "Strategic", "Fundamental", "Mean", or "Uncategorized"
        level (int, optional): level of markdown main section (2 sub-levels are added).
        Defaults to 1.

    Returns:
        str: a markdown representation of the objective data for one given category
    """
    md = ""
    if data[category]:
        md += header(level=level + 2, prefix=category)
        md += unordered_list(item["description"] for item in data[category])
    return md


def generate_objective_data(data: list, level=1) -> str:
    """generate the objective data in markdown format

    Args:
        data (list): objective data from database
        level (int, optional): level of markdown section. Defaults to 1.

    Returns:
        str: a markdown representation of the objective data
    """
    grouped_data = group_objectives(data)
    md = ""
    md += header(level=level + 1, prefix="Objectives")
    for k in ["Strategic", "Fundamental", "Mean", "Uncategorized"]:
        md += add_objectives(grouped_data, k, level)
    return md
