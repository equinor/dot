import pytest
import numpy as np

from src.pgm.probabilistic_graph_models import (Variable,
                                                Node,
                                                Arc,
                                                Graph,
                                                CPD,
                                                ProbGraphModel,
                                                ModelABC,
                                                )


@pytest.fixture
def network():
    var_pollution = Variable("Pollution", ["yes", "no"], "chance")
    var_smoker = Variable("Smoker", ["yes", "no"], "chance")
    var_cancer = Variable("Cancer", ["yes", "no"], "chance")
    var_xray = Variable("Xray", ["yes", "no"], "chance")
    var_dyspnoea = Variable("Dyspnoea", ["yes", "no"], "chance")

    node_pollution = Node("Pollution")
    node_smoker = Node("Smoker")
    node_cancer = Node("Cancer")
    node_xray = Node("Xray")
    node_dyspnoea = Node("Dyspnoea")

    cpd_pollution = CPD(
        variable=var_pollution,
        parents=None,
        table=[[0.9],
            [0.1]],
        )
    cpd_smoker = CPD(
        variable=var_smoker,
        parents=None,
        table=[[0.3],
            [0.7]],
        )
    cpd_cancer = CPD(
        variable=var_cancer,
        parents=[var_smoker, var_pollution],
        table=[[0.03, 0.05, 0.001, 0.02],
            [0.97, 0.95, 0.999, 0.98]],
    )
    cpd_xray = CPD(
        variable=var_xray,
        parents=[var_cancer],
        table=[[0.9, 0.2],
            [0.1, 0.8]],
    )
    cpd_dyspnoea = CPD(
        variable=var_dyspnoea,
        parents=[var_cancer],
        table=[[0.65, 0.3],
            [0.35, 0.7]],
    )

    variables = (
        var_pollution,
        var_smoker,
        var_cancer,
        var_xray,
        var_dyspnoea,
    )

    nodes = (
        node_pollution,
        node_smoker,
        node_cancer,
        node_xray,
        node_dyspnoea,
    )

    arcs = (
        Arc(node_pollution, node_cancer),
        Arc(node_smoker, node_cancer),
        Arc(node_cancer, node_xray),
        Arc(node_cancer, node_dyspnoea),
    )

    graph = Graph(nodes, arcs)

    cpds = (
        cpd_pollution,
        cpd_smoker,
        cpd_cancer,
        cpd_xray,
        cpd_dyspnoea,
    )

    return ProbGraphModel(
        name="cancer model",
        variables=variables,
        graph=graph,
        potentials=cpds
    )


def test_class_ProbGraphModel(network):
    assert network.name == "cancer model"
    assert len(network.variables) == 5


def test_class_ProbGraphModel_print_variables(network, capsys):
    network.print_variables()
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
    network.print_nodes()
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
    network.print_arcs()
    captured = capsys.readouterr()
    assert captured.out == (
        "Arcs:\n"
        "('Pollution', 'Cancer')\n"
        "('Smoker', 'Cancer')\n"
        "('Cancer', 'Xray')\n"
        "('Cancer', 'Dyspnoea')\n\n\n"
        )


def test_class_ProbGraphModel_print_potentials(network, capsys):
    network.print_potentials()
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
    assert network.get_potential_by_name("junk") is None

    potential = network.get_potential_by_name("Cancer")
    assert potential.variable.name == "Cancer"
    assert potential.variable.states == ['yes', 'no']
    assert potential.variable.type == "chance"
    assert len(potential.parents) == 2
    assert potential.parents[0].name == "Smoker"
    assert potential.parents[1].name == "Pollution"
    assert potential.table == [[0.03, 0.05, 0.001, 0.02], [0.97, 0.95, 0.999, 0.98]]


def test_class_ProbGraphModel_get_variable_by_name(network):
    assert network.get_variable_by_name("junk") is None

    variable = network.get_variable_by_name("Smoker") 
    assert variable.name == "Smoker"
    assert variable.states == ["yes", "no"]
    assert variable.type == "chance"


def test_class_ProbGraphModel_to_valid(network):
    assert network._to_valid("  90sd as%/'qq21  ") == "_90sd_as_qq21_"


def test_class_ProbGraphModel_potential_to_xarray(network):
    xarr = network.potential_to_xarray("Cancer")
    np.testing.assert_allclose(xarr.data, [[[0.03, 0.05], [0.001, 0.02]],
                                           [[0.97, 0.95], [0.999, 0.98]]])
    assert xarr.sel(Cancer="yes", Smoker="no", Pollution="yes") == 0.001


def test_class_ModelABC(monkeypatch, network):
    monkeypatch.setattr(
        ModelABC,
        "__abstractmethods__",
        set(),
    )
    model = ModelABC(network=network)
    with pytest.raises(NotImplementedError):
        model.modelling()
    with pytest.raises(NotImplementedError):
        model.copy(None)
    with pytest.raises(NotImplementedError):
        model.get_potentials("junk")
    with pytest.raises(NotImplementedError):
        model.draw_graph()
    with pytest.raises(NotImplementedError):
        model.inference(None)


