from unittest.mock import patch
from uuid import uuid4
import pytest

from src.v0.services.reporting_utils.markdown_report import MarkdownReport, generate_report, pypandoc


def test_MarkdownReport(capsys):
    mdr = MarkdownReport()
    assert mdr._md == ""
    print(mdr.update("junk"))
    captured = capsys.readouterr()
    assert captured.out == "junk\n\n"
    assert repr(mdr) == "md is\njunk\n"


def test_convert_unknown(capsys):
    mdr = MarkdownReport()
    mdr.update("junk")
    captured = capsys.readouterr()
    uuid = uuid4()
    mdr.convert(f"probably_a_format_that_will_never_exist_{uuid}")
    captured = capsys.readouterr()
    assert captured.out.startswith("Unknown output format")
    assert captured.out.endswith("Check pypandoc for help.\n")


@patch("src.v0.services.reporting_utils.markdown_report.pypandoc.convert_text")
def test_convert_docx(mocker):
    mdr = MarkdownReport()
    mdr.update("junk")
    mdr.convert("doc")
    mocker.assert_called_once_with("junk\n", "docx", "md")


def test_MarkdownReport_write(capsys):
    mdr = MarkdownReport()
    mdr.update("junk")
    mdr.write()
    captured = capsys.readouterr()
    assert captured.out == "junk\n"
    
