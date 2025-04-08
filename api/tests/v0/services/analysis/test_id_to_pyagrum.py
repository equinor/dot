import json

import numpy as np
import pyAgrum as gum
import pytest

from src.v0.services.analysis.id_to_pyagrum import InfluenceDiagramToPyAgrum
from src.v0.services.classes.arc import Arc
from src.v0.services.classes.discrete_unconditional_probability import (
    DiscreteUnconditionalProbability,
)
from src.v0.services.format_conversions.directed_graph import InfluenceDiagramConversion

TESTDATA = "v0/services/testdata"


@pytest.fixture
def influence_diagram(copy_testdata_tmpdir, tmp_path):
    copy_testdata_tmpdir(TESTDATA)
    with open(tmp_path / "used_car_buyer_problem.json") as f:
        data = json.load(f)
    issues = data["vertices"]["issues"]
    issues = [
        {"uuid" if k == "id" else k: v for k, v in issue.items()} for issue in issues
    ]
    data = {
        "vertices": issues,
        "edges": [edge for edge in data["edges"] if edge["label"] == "influences"],
    }
    diagram = InfluenceDiagramConversion().from_json(data)
    return diagram


def test_conversion_used_car_buyer_success(influence_diagram):
    result = InfluenceDiagramToPyAgrum().conversion(influence_diagram)
    assert isinstance(result, gum.InfluenceDiagram)
    assert result.size() == 5
    assert result.chanceNodeSize() == 2
    assert result.decisionNodeSize() == 2
    assert result.utilityNodeSize() == 1

    # import pyAgrum.lib.image as gimg
    # from shutil import copyfile
    # gimg.export(result, "test2.png")
    # result.saveBIFXML("test.bifxml")
    # testroot = '/tmp/pytest-of-codespace/pytest-current/'
    # testpath = testroot+'test_conversion_used_car_buyercurrent/'
    # copyfile(testpath+"test2.png", "/workspaces/dot/test2.png")
    # copyfile(testpath+"test.bifxml", "/workspaces/dot/test.bifxml")


def test_to_pyagrum_used_car_buyer_not_acyclic_fail(influence_diagram, caplog):
    node0 = list(influence_diagram.graph.nodes)[0]
    node1 = list(influence_diagram.graph.nodes)[1]
    edge1 = Arc(tail=node0, head=node1, label="cyclic")
    edge2 = Arc(tail=node1, head=node0, label="cyclic")
    influence_diagram.add_arc(edge1)
    influence_diagram.add_arc(edge2)

    with pytest.raises(Exception) as exc_info:
        InfluenceDiagramToPyAgrum().conversion(influence_diagram)
    assert [r.msg for r in caplog.records] == [
        "the influence diagram is not acyclic: False"
    ]
    assert str(exc_info.value) == "the influence diagram is not acyclic: False"


def test_to_pyagrum_used_car_buyer_uncertainty_2d_unconditional_fail(
    influence_diagram, caplog
):
    for node in influence_diagram.nodes:
        node.probability = DiscreteUnconditionalProbability(
            **{
                "probability_function": np.array([[0.1, 0.2], [0.3, 0.4]]),
                "variables": {"v1": ["blue", "green"], "v2": ["high", "low"]},
            }
        )
    with pytest.raises(Exception) as exc_info:
        InfluenceDiagramToPyAgrum().conversion(influence_diagram)
    assert (
        "Input probability cannot be used in pyagrum with error:"
        in [r.msg for r in caplog.records][0]
    )
    assert "Input probability cannot be used in pyagrum with error:" in str(
        exc_info.value
    )


def test_to_pyagrum_used_car_buyer_uncertainty_fail(influence_diagram, caplog):
    for node in influence_diagram.nodes:
        node.probability = None
    with pytest.raises(Exception) as exc_info:
        InfluenceDiagramToPyAgrum().conversion(influence_diagram)
    assert [r.msg for r in caplog.records] == [
        (
            "Input probability cannot be used in pyagrum with error: [pyAgrum] "
            "Invalid argument: Empty variable State:Labelized({}) "
            "cannot be added in a Potential"
        )
    ]
    assert str(exc_info.value) == (
        "Input probability cannot be used in pyagrum with error: [pyAgrum] "
        "Invalid argument: Empty variable State:Labelized({}) "
        "cannot be added in a Potential"
    )


def test_to_pyagrum_used_car_buyer_decision_fail(influence_diagram, caplog):
    for node in influence_diagram.nodes:
        node.alternatives = None

    with pytest.raises(Exception) as exc_info:
        InfluenceDiagramToPyAgrum().conversion(influence_diagram)
    assert [r.msg for r in caplog.records] == [
        "Input arc cannot be used in pyagrum with error: "
        "[pyAgrum] Invalid argument: Empty variable Test:Labelized({}) "
        "cannot be added in a Potential"
    ]
    assert str(exc_info.value) == (
        "Input arc cannot be used in pyagrum with error: "
        "[pyAgrum] Invalid argument: Empty variable Test:Labelized({}) "
        "cannot be added in a Potential"
    )
