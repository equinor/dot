"""
Module for making a markdown report
"""

import sys
from pathlib import Path

import pypandoc

from .markdown_elements import one_newline
from .markdown_issue import generate_issue_data
from .markdown_objective import generate_objective_data
from .markdown_opportunity import generate_opportunity_data
from .markdown_project import generate_project_data


class MarkdownReport:
    """Class for generating a markdown file

    There is only one attribute `_md` containing the current markdown as a string
    """

    def __init__(self):
        self._md = ""

    def update(self, data: str):
        """update the markdown content

        Args:
            data (str): data to add to the markdown
        """
        self._md += data
        self._md += one_newline
        return self

    def write(self, filepath: Path = "-", template: Path = None):
        """Write markdown

        Args:
            filepath (Path, optional): file to write the markdown to. The extension
            specifies the format of the output file. Defaults to "-", meaning print in
            terminal.
            template (Path, optional): template file to use for conversion.
            Defaults to None, meaning no specific template is used.

        Raises:
            ValueError: when the markdown content cannot be converted into the required
            format
        """
        if filepath == "-":
            sys.stdout.write(self._md)
            return None
        fmt = Path(filepath).suffix
        try:
            conversion_args = [
                self._md,
                fmt[1:],
                "md",
            ]
            conversion_kwargs = {
                "outputfile": Path(filepath).with_suffix(fmt)
                }
            if template and fmt[1:] in ["docx", "odt", "pptx"]:
                conversion_kwargs["extra_args"] = [f"--reference-doc={template}"]
            pypandoc.convert_text(
                *conversion_args,
                **conversion_kwargs,

            )
        except Exception as e:
            raise ValueError(f"Cannot convert into {fmt[1:]} format: {e}")

    def __str__(self):
        return f"{self._md}"

    def __repr__(self):
        return f"md is\n{self._md}"


def generate_report(data: dict, level=1, filepath="-", template: str = None):
    """Generate the report given a dictionary represneting the project

    Args:
        data (dict): project data
        level (int, optional): level of the main section. Defaults to 1.
        filepath (str, optional): output filepath. Defaults to "-", meaning
        display in terminal only.
        template (str, optional): template for output file (e.g. MS office files).
        Defaults to None, meaning no template.

    Returns:
        _type_: _description_
    """
    md_document = MarkdownReport()
    md_document.update(generate_project_data(data["project"], level))
    md_document.update(generate_opportunity_data(data["opportunities"], level + 1))
    md_document.update(generate_objective_data(data["objectives"], level + 1))
    md_document.update(generate_issue_data(data["issues"], level + 1))
    md_document.write(filepath, template)
    return None
