import logging

from src.common import logger


def test_set_up_logger():
    result = logger.set_up_logger("junk")
    assert result.name == "junk"
    assert result.level == logging.DEBUG
