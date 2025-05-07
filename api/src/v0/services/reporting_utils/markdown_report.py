"""
Module for making a markdown report
"""
from pathlib import Path
import sys
import pypandoc

from .markdown_elements import one_newline
from .markdown_issue import generate_issue_data
from .markdown_objective import generate_objective_data
from .markdown_opportunity import generate_opportunity_data
from .markdown_project import generate_project_data


class MarkdownReport:
    def __init__(self):
        self._md = ""

    def update(self, data: str):
        self._md += data
        self._md += one_newline
        return self
    
    def convert(self, fmt):
        if fmt in ["doc", "docx"]:
            return pypandoc.convert_text(
                self._md, "docx", "md"
            )
        print(f"Unknown output format {fmt}. Check pypandoc for help.")

    def write(self, filepath: Path="-", fmt="md"):
        if filepath == "-":
            sys.stdout.write(self._md)
            return None
        with open(filepath, "w") as f:
                f.write(self._md)
        return None

    def __str__(self):
        return f"{self._md}"

    def __repr__(self):
        return f"md is\n{self._md}"


def generate_report(data: dict, level=1, filepath="-", doc=True):
    md_document = MarkdownReport()
    md_document.update(generate_project_data(data["project"], level))
    md_document.update(generate_opportunity_data(data["opportunities"], level + 1))
    md_document.update(generate_objective_data(data["objectives"], level + 1))
    md_document.update(generate_issue_data(data["issues"], level + 1))
    md_document.write(filepath, doc)
