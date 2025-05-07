import pytest

from src.v0.services.reporting_utils.markdown_report import MarkdownReport, generate_report


def test_MarkdownReport(capsys):
    mdr = MarkdownReport()
    assert mdr._md == ""
    print(mdr.update("junk"))
    captured = capsys.readouterr()
    assert captured.out == "junk\n\n"
    assert repr(mdr) == "md is\njunk\n"

def test_MarkdownReport_write(capsys):
    mdr = MarkdownReport()
    mdr.update("junk")
    mdr.write()
    captured = capsys.readouterr()
    assert captured.out == "junk\n"
    
