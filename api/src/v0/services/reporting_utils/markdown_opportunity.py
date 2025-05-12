"""
Module for converting the opportunity data into markdown
"""

from .markdown_elements import header, unordered_list


def generate_opportunity_data(data: list, level=1) -> str:
    """generate the opportunity data in markdown format

    Args:
        data (list): opportunity data from database
        level (int, optional): level of markdown section. Defaults to 1.

    Returns:
        str: a markdown representation of the opportunity data
    """
    md = ""
    md += header(level=level + 1, prefix="Opportunity statements")
    md += unordered_list(item["description"] for item in data)
    return md
