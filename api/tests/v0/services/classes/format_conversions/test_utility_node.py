import pytest

from src.v0.services.classes.format_conversions.node import UtilityNodeConversion
from src.v0.services.classes.node import UtilityNode


@pytest.fixture
def utility_node():
    return {
        "description": "testing node",
        "shortname": "Node",
        "boundary": "in",
        "comments": [{
            "author": "Jr.",
            "comment": "Nope"
        }],
        "category": "Value Metric",
        "uuid": "a6ab145e-2ca9-49e2-8c4f-9607688e57a9"
        }



def test_class_UtilityNodeConversion_from_json_fail(caplog):
    as_json = {
        "category": "Junk",
        "description": "C2H5OH",
        "shortname": "veni vidi vici",
        }
    with pytest.raises(Exception) as exc_info:
        UtilityNodeConversion().from_json(as_json)
    assert [r.msg for r in caplog.records] == \
        ["Data cannot be used to create a UtilityNode."]
    assert str(exc_info.value) == \
        "Data cannot be used to create a UtilityNode."


def test_UtilityNodeConversion_from_json(utility_node):
    result = UtilityNodeConversion().from_json(utility_node)
    assert isinstance(result, UtilityNode)
    assert result.description == "testing node"
    assert result.shortname == "Node"


def test_UtilityNodeConversion_to_json(utility_node):
    data = UtilityNode(
        description=utility_node['description'],
        shortname=utility_node['shortname']
        )
    result = UtilityNodeConversion().to_json(data)
    assert result['description'] == utility_node['description']
    assert result['shortname'] == utility_node['shortname']
    assert result['uuid'] == data.uuid
