from uuid import UUID, uuid4

import numpy as np
import pytest

from src.v0.services.classes.discrete_unconditional_probability import (
    DiscreteUnconditionalProbability,
)
from src.v0.services.classes.validations import validate_and_set_node


def test_description_success():
    assert validate_and_set_node.description("None") == "None"


def test_description_fail(caplog):
    with pytest.raises(Exception) as exc_info:
        validate_and_set_node.description(None)
    assert [r.msg for r in caplog.records] == ["Input description is not a string."]
    assert str(exc_info.value) == "Input description is not a string."


def test_name_success():
    assert validate_and_set_node.name("None") == "None"


def test_name_fail(caplog):
    with pytest.raises(Exception) as exc_info:
        validate_and_set_node.name(None)
    assert [r.msg for r in caplog.records] == ["Input name is not a string."]
    assert str(exc_info.value) == "Input name is not a string."


def test_shortname_success():
    assert validate_and_set_node.shortname("None") == "None"


def test_shortname_fail(caplog):
    with pytest.raises(Exception) as exc_info:
        validate_and_set_node.shortname(None)
    assert [r.msg for r in caplog.records] == ["Input shortname is not a string."]
    assert str(exc_info.value) == "Input shortname is not a string."


def test_uuid_success_uuid():
    id = uuid4()
    assert isinstance(validate_and_set_node.uuid(id), str)
    assert UUID(validate_and_set_node.uuid(id)).version == 4
    assert isinstance(validate_and_set_node.uuid(str(id)), str)
    assert UUID(validate_and_set_node.uuid(str(id))).version == 4


def test_uuid_success_None():
    assert UUID(validate_and_set_node.uuid(None)).version == 4


def test_uuid_fail_not_None(caplog):
    with pytest.raises(Exception) as exc_info:
        validate_and_set_node.uuid(3.14)
    assert [r.msg for r in caplog.records] == [("Input uuid is neither a "
                                                "valid uuid (version 4) nor None.")]
    assert str(exc_info.value) == ("Input uuid is neither a "
                                   "valid uuid (version 4) nor None.")


def test_uuid_fail_not_uuid4(caplog):
    with pytest.raises(Exception) as exc_info:
        validate_and_set_node.uuid("3.14")
    assert [r.msg for r in caplog.records] == [("Input uuid is neither a "
                                                "valid uuid (version 4) nor None.")]
    assert str(exc_info.value) == ("Input uuid is neither a "
                                   "valid uuid (version 4) nor None.")


def test_alternatives_success_list_of_strings():
    assert validate_and_set_node.alternatives(["1", "2", "3"]) == ["1", "2", "3"]


def test_alternatives_success_tuple_of_strings():
    assert validate_and_set_node.alternatives(("1", "2", "3")) == ("1", "2", "3")


def test_alternatives_success_None():
    assert validate_and_set_node.alternatives(None) is None


def test_alternatives_fail_string(caplog):
    with pytest.raises(Exception) as exc_info:
        validate_and_set_node.alternatives("3.14")
    assert [r.msg for r in caplog.records] == [
        "Input alternatives is neither a list or tuple of unique strings nor None."
    ]
    assert str(exc_info.value) == \
        "Input alternatives is neither a list or tuple of unique strings nor None."


def test_alternatives_fail_not_sequence(caplog):
    with pytest.raises(Exception) as exc_info:
        validate_and_set_node.alternatives({"3.14"})
    assert [r.msg for r in caplog.records] == [
        "Input alternatives is neither a list or tuple of unique strings nor None."
    ]
    assert str(exc_info.value) == \
        "Input alternatives is neither a list or tuple of unique strings nor None."


def test_alternatives_fail_list_of_lists(caplog):
    with pytest.raises(Exception) as exc_info:
        validate_and_set_node.alternatives([["3.14"]])
    assert [r.msg for r in caplog.records] == [
        "Input alternatives is neither a list or tuple of unique strings nor None."
    ]
    assert str(exc_info.value) == \
        "Input alternatives is neither a list or tuple of unique strings nor None."


def test_alternatives_fail_redundant_elements(caplog):
    with pytest.raises(Exception) as exc_info:
        validate_and_set_node.alternatives(["a", "a", "b"])
    assert [r.msg for r in caplog.records] == [
        "Input alternatives is neither a list or tuple of unique strings nor None."
    ]
    assert str(exc_info.value) == \
        "Input alternatives is neither a list or tuple of unique strings nor None."


def test_probability_success_None():
    assert validate_and_set_node.probability(None) is None


def test_probability_success_well_formed_probability():
    values = np.array([0.1, 0.9])
    coords = {"A": ["yes", "no"]}
    probability = DiscreteUnconditionalProbability(values, coords)
    assert validate_and_set_node.probability(probability) == probability


def test_alternatives_fail_neither_None_nor_well_formed_probability(caplog):
    with pytest.raises(Exception) as exc_info:
        validate_and_set_node.probability([["3.14"]])
    assert [r.msg for r in caplog.records] == \
        ["Input probability is neither a well formed probability nor None."]
    assert str(exc_info.value) == \
        "Input probability is neither a well formed probability nor None."
