from unittest.mock import patch, mock_open
import json

import pytest
import numpy as np

from src.pgm.probabilistic_graph_models import ProbGraphModel, ModelABC


@pytest.fixture
def network():
    data = {
       "name": "Cancer model",
       "variables": [
           {
               "name": "Pollution",
                "states": ["yes", "no"],
                "type": "chance"
                },
           {
               "name": "Smoker",
                "states": ["yes", "no"],
                "type": "chance"
                },
           {
               "name": "Cancer",
                "states": ["yes", "no"],
                "type": "chance"
                },
           {
               "name": "Xray",
                "states": ["yes", "no"],
                "type": "chance"
                },
           {
               "name": "Dyspnoea",
                "states": ["yes", "no"],
                "type": "chance"
                },
       ],
       "nodes": ["Pollution", "Smoker", "Cancer", "Xray", "Dyspnoea"],
       "arcs": [
          ["Pollution", "Cancer"],
          ["Smoker", "Cancer"],
          ["Cancer", "Xray"],
          ["Cancer", "Dyspnoea"]
       ],
       "potentials": [
          {
             "variable": "Pollution",
             "parents": None,
             "table": [[0.9], [0.1]],
             "type": "cpd"
             },
          {
             "variable": "Smoker",
             "parents": None,
             "table": [[0.3], [0.7]],
             "type": "cpd"
             },
          {
             "variable": "Cancer",
             "parents": ["Smoker", "Pollution"],
             "table": [[0.03, 0.05, 0.001, 0.02], [0.97, 0.95, 0.999, 0.98]],
             "type": "cpd"
             },
          {
             "variable": "Xray",
             "parents": ["Cancer"],
             "table": [[0.9, 0.2], [0.1, 0.8]],
             "type": "cpd"
             },
          {
             "variable": "Dyspnoea",
             "parents": ["Cancer"],
             "table": [[0.65, 0.3], [0.35, 0.7]],
             "type": "cpd"
             },
       ]
    }
    return data


def test_class_ProbGraphModel(network):
    model = ProbGraphModel.read_model(network)
    assert model.name == "Cancer model"
    assert len(model.variables) == 5


def test_class_ProbGraphModel_dict_to_potentials():
    variables = [
        {
            "name": "Car state",
            "states": ["lemon", "peach"],
            "type": "chance"
            },
        {
            "name": "Purchase",
            "states": ["buy without guarantee", "buy with guarantee", "don't buy"],
            "type": "decision"
            },
        {
            "name": "Repair costs",
            "states": [],
            "type": "value"
            }
            ]
    potentials = [
        {
            "variable": "Repair costs",
            "parents": ["Car state", "Purchase"],
            "table": [[-200, 0, 0], [-40, -20, 0]],
            "type": "utility"
        }
        ]
    variables = ProbGraphModel._dict_to_variables(variables)
    results = ProbGraphModel._dict_to_potentials(variables, potentials)
    assert results[0].table == [[-200, 0, 0], [-40, -20, 0]]


def test_class_ProbGraphModel_read_model_from_file(network):
    with patch("builtins.open", mock_open(read_data=json.dumps(network))) as mock_file:
        ProbGraphModel.read_model("junk.yaml")
    mock_file.assert_called_once_with("junk.yaml", "r")


def test_class_ProbGraphModel_print_variables(network, capsys):
    model = ProbGraphModel.read_model(network)
    model.print_variables()
    captured = capsys.readouterr()
    assert captured.out == (
        "Variables:\n"
        "Variable(name='Pollution', states=['yes', 'no'], type='chance')\n"
        "Variable(name='Smoker', states=['yes', 'no'], type='chance')\n"
        "Variable(name='Cancer', states=['yes', 'no'], type='chance')\n"
        "Variable(name='Xray', states=['yes', 'no'], type='chance')\n"
        "Variable(name='Dyspnoea', states=['yes', 'no'], type='chance')\n\n\n"
        )


def test_class_ProbGraphModel_print_nodes(network, capsys):
    model = ProbGraphModel.read_model(network)
    model.print_nodes()
    captured = capsys.readouterr()
    assert captured.out == (
        "Nodes:\n"
        "Pollution\n"
        "Smoker\n"
        "Cancer\n"
        "Xray\n"
        "Dyspnoea\n\n\n"
        )


def test_class_ProbGraphModel_print_arcs(network, capsys):
    model = ProbGraphModel.read_model(network)
    model.print_arcs()
    captured = capsys.readouterr()
    assert captured.out == (
        "Arcs:\n"
        "('Pollution', 'Cancer')\n"
        "('Smoker', 'Cancer')\n"
        "('Cancer', 'Xray')\n"
        "('Cancer', 'Dyspnoea')\n\n\n"
        )


def test_class_ProbGraphModel_print_potentials(network, capsys):
    model = ProbGraphModel.read_model(network)
    model.print_potentials()
    captured = capsys.readouterr()
    assert captured.out == (
        "Potentials:\n"
        "CPD("
        "variable=Variable(name='Pollution', states=['yes', 'no'], type='chance'), "
        "parents=None, "
        "table=[[0.9], [0.1]])\n"
        "CPD("
        "variable=Variable(name='Smoker', states=['yes', 'no'], type='chance'), "
        "parents=None, "
        "table=[[0.3], [0.7]])\n"
        "CPD("
        "variable=Variable(name='Cancer', states=['yes', 'no'], type='chance'), "
        "parents=["
        "Variable(name='Smoker', states=['yes', 'no'], type='chance'), "
        "Variable(name='Pollution', states=['yes', 'no'], type='chance')], "
        "table=[[0.03, 0.05, 0.001, 0.02], [0.97, 0.95, 0.999, 0.98]])\n"
        "CPD("
        "variable=Variable(name='Xray', states=['yes', 'no'], type='chance'), "
        "parents=[Variable(name='Cancer', states=['yes', 'no'], type='chance')], "
        "table=[[0.9, 0.2], [0.1, 0.8]])\n"
        "CPD("
        "variable=Variable(name='Dyspnoea', states=['yes', 'no'], type='chance'), "
        "parents=[Variable(name='Cancer', states=['yes', 'no'], type='chance')], "
        "table=[[0.65, 0.3], [0.35, 0.7]])\n\n\n"
        )
    

def test_class_ProbGraphModel_get_potential_by_name(network):
    model = ProbGraphModel.read_model(network)
    assert model.get_potential_by_name("junk") is None

    potential = model.get_potential_by_name("Cancer")
    assert potential.variable.name == "Cancer"
    assert potential.variable.states == ['yes', 'no']
    assert potential.variable.type == "chance"
    assert len(potential.parents) == 2
    assert potential.parents[0].name == "Smoker"
    assert potential.parents[1].name == "Pollution"
    assert potential.table == [[0.03, 0.05, 0.001, 0.02], [0.97, 0.95, 0.999, 0.98]]


def test_class_ProbGraphModel_get_variable_by_name(network):
    model = ProbGraphModel.read_model(network)
    assert model.get_variable_by_name("junk") is None

    variable = model.get_variable_by_name("Smoker") 
    assert variable.name == "Smoker"
    assert variable.states == ["yes", "no"]
    assert variable.type == "chance"


def test_class_ProbGraphModel_to_valid(network):
    model = ProbGraphModel.read_model(network)
    assert model._to_valid("  90sd as%/'qq21  ") == "_90sd_as_qq21_"


def test_class_ProbGraphModel_potential_to_xarray(network):
    model = ProbGraphModel.read_model(network)
    xarr = model.potential_to_xarray("Cancer")
    np.testing.assert_allclose(xarr.data, [[[0.03, 0.05], [0.001, 0.02]],
                                           [[0.97, 0.95], [0.999, 0.98]]])
    assert xarr.sel(Cancer="yes", Smoker="no", Pollution="yes") == 0.001


def test_class_ModelABC(monkeypatch, network):
    monkeypatch.setattr(
        ModelABC,
        "__abstractmethods__",
        set(),
    )
    graph_model = ProbGraphModel.read_model(network)
    model = ModelABC(network=graph_model)
    with pytest.raises(NotImplementedError):
        model.modelling()
    with pytest.raises(NotImplementedError):
        model.copy()
    with pytest.raises(NotImplementedError):
        model.get_potential("junk")
    with pytest.raises(NotImplementedError):
        model.draw_graph()
    with pytest.raises(NotImplementedError):
        model.inference()
    with pytest.raises(NotImplementedError):
        model.posterior(None)

