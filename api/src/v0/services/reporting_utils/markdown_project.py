"""
Module for converting the project data into markdown
"""

from .markdown_elements import header, table_section, text_line


def project_description(data: dict, level=1) -> str:
    """convert the project description into markdown

    Args:
        data (dict): project data from database
        level (int, optional): level of markdown section. Defaults to 1.

    Returns:
        str: a markdown section for the project description
    """
    md = ""
    md += header(level=level + 1, prefix="Description")
    md += text_line(data=data["description"])
    return md


def project_information(data: dict, level=1) -> str:
    """convert some key project information into markdown

    Args:
        data (dict): project data from database
        level (int, optional): level of markdown section. Defaults to 1.

    Returns:
        str: a markdown section for the project key information
    """
    md = ""
    md += table_section(
        level=level + 1,
        header_data=("Key information", None),
        data=data,
        filter_keys=["decision_maker", "decision_date", "sensitivity_label"],
    )
    return md


def generate_project_data(data: dict, level=1) -> str:
    """generate the project data in markdown format

    Args:
        data (dict): project data from database
        level (int, optional): level of markdown section. Defaults to 1.

    Returns:
        str: a markdown representation of the project data
    """
    md = ""
    md += header(level=level, prefix="Project", data=data["name"])
    md += project_description(data, level)
    md += project_information(data, level)
    return md
