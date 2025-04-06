from uuid import UUID, uuid1, uuid4

import pytest

from src.v0.services.classes.node import DecisionNode
from src.v0.services.classes.validations import validate_and_set_arc


def test_label_success_string():
    assert validate_and_set_arc.label("None") == "None"


def test_label_success_None():
    assert validate_and_set_arc.label(None) is None


def test_label_fail(caplog):
    with pytest.raises(Exception) as exc_info:
        validate_and_set_arc.label(1.0)
    assert [r.msg for r in caplog.records] == [
        "Input label is neither a string nor None: 1.0"
    ]
    assert str(exc_info.value) == "Input label is neither a string nor None: 1.0"


def test_edge_success_None():
    assert validate_and_set_arc.edge(None) is None


def test_edge_success_Node():
    node = DecisionNode(description="decision", shortname="D")
    assert isinstance(validate_and_set_arc.edge(node), DecisionNode)


def test_edge_fail_neither_Node_nor_None(caplog):
    with pytest.raises(Exception) as exc_info:
        validate_and_set_arc.edge(1.0)
    assert [r.msg for r in caplog.records] == [
        "Endpoint of arcs should be Node or None: 1.0"
    ]
    assert str(exc_info.value) == "Endpoint of arcs should be Node or None: 1.0"


def test_uuid_success_uuid():
    id = uuid4()
    assert isinstance(validate_and_set_arc.uuid(id), str)
    assert UUID(validate_and_set_arc.uuid(id)).version == 4
    assert isinstance(validate_and_set_arc.uuid(str(id)), str)
    assert UUID(validate_and_set_arc.uuid(str(id))).version == 4


def test_uuid_success_None():
    assert UUID(validate_and_set_arc.uuid(None)).version == 4


def test_uuid_fail_not_None(caplog):
    with pytest.raises(Exception) as exc_info:
        validate_and_set_arc.uuid(3.14)
    assert [r.msg for r in caplog.records] == [
        "Input uuid is neither a valid uuid (version 4) nor None: 3.14"
    ]
    assert (
        str(exc_info.value)
        == "Input uuid is neither a valid uuid (version 4) nor None: 3.14"
    )


def test_uuid_fail_not_uuid(caplog):
    with pytest.raises(Exception) as exc_info:
        validate_and_set_arc.uuid("3.14")
    assert [r.msg for r in caplog.records] == [
        (
            "Input uuid is neither a valid uuid (version 4) nor None: "
            "badly formed hexadecimal UUID string"
        )
    ]
    assert str(exc_info.value) == (
        "Input uuid is neither a valid uuid (version 4) nor None: "
        "badly formed hexadecimal UUID string"
    )


def test_uuid_fail_not_version_4(caplog):
    id = str(uuid1())
    with pytest.raises(Exception) as exc_info:
        validate_and_set_arc.uuid(id)
    assert [r.msg for r in caplog.records] == [
        ("Input uuid is neither a valid " "uuid (version 4) nor None: version 1")
    ]
    assert str(exc_info.value) == (
        "Input uuid is neither a valid " "uuid (version 4) nor None: version 1"
    )
