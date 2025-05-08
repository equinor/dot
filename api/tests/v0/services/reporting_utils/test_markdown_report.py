from pathlib import PosixPath
from unittest.mock import patch

import pytest

from src.v0.services.reporting_utils.markdown_report import (
    MarkdownReport,
    generate_report,
)


def test_MarkdownReport(capsys):
    mdr = MarkdownReport()
    assert mdr._md == ""
    print(mdr.update("junk"))
    captured = capsys.readouterr()
    assert captured.out == "junk\n\n"
    assert repr(mdr) == "md is\njunk\n"


def test_MarkdownReport_write_to_terminal(capsys):
    mdr = MarkdownReport()
    mdr.update("junk")
    mdr.write()
    captured = capsys.readouterr()
    assert captured.out == "junk\n"


@patch("src.v0.services.reporting_utils.markdown_report.pypandoc.convert_text")
def test_write_to_docx(mocker):
    mdr = MarkdownReport()
    mdr.update("junk")
    mdr.write("junk.docx")
    mocker.assert_called_once_with(
        "junk\n", "docx", "md", outputfile=PosixPath("junk.docx")
    )


def test_write_fail():
    mdr = MarkdownReport()
    mdr.update("junk")
    with pytest.raises(Exception) as exc:
        mdr.write("junk.an_extension_which_will_probably_never_exist")
    assert (
        "Cannot convert into an_extension_which_will_probably_never_exist format: "
        in str(exc.value)
    )


def test_generate_report(capsys):
    data = {
        "project": {
            "name": "the little project example",
            "description": "This is a project example",
            "tag": ["subsurface"],
            "decision_maker": "John Doe",
            "decision_date": "2021-01-01",
            "sensitivity_label": "Restricted",
            "index": "0",
        },
        "opportunities": [],
        "objectives": [],
        "issues": [],
    }
    generate_report(data, filepath="-")
    captured = capsys.readouterr()
    assert captured.out.startswith("# Project: the little project example \n\n")
