"""
Module for making a markdown report
"""
from .markdown_elements import one_newline
from .markdown_project import generate_project_data
from .markdown_opportunity import generate_opportunity_data
from .markdown_objective import generate_objective_data
from .markdown_issue import generate_issue_data


class MarkdownReport:
    def __init__(self):
        self._md = ""

    def update(self, data: str):
        self._md += data
        self._md += one_newline
        return self

    # def write(self, filepath: Path, doc: bool):
    #     if filepath == "-":
    #         sys.stdout.write(self._md)
    #     else:
    #         with click.open_file(filepath + ".md", "w") as f:
    #             f.write(self._md)
    #         if doc:
    #             pypandoc.convert_file(
    #                 filepath + ".md", "docx", outputfile=filepath + ".docx"
    #             )

    #     return None

    def __str__(self):
        return self._md

    def __repr__(self):
        return self._md
    


def generate_report(data: dict, level=1):
    md_document = MarkdownReport()
    md_document.update(generate_project_data(data["project"], level))
    md_document.update(generate_opportunity_data(data["opportunities"], level + 1))
    md_document.update(generate_objective_data(data["objectives"], level + 1))
    md_document.update(generate_issue_data(data["issues"], level + 1))    