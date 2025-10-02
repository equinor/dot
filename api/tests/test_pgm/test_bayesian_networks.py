from unittest.mock import patch, MagicMock

import pytest
import numpy as np

from src.pgm.probabilistic_graph_models import ProbGraphModel
from src.pgm.bayesian_networks import BNPGM, DiscreteBayesianNetwork, BNGUM, gum


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


def test_class_BNPGM(network):
   model = ProbGraphModel.read_model(network)
   model = BNPGM(network=model)
   assert isinstance(model.model, DiscreteBayesianNetwork)
   assert list(model.model.edges) == [
       ('Pollution', 'Cancer'),
       ('Cancer', 'Xray'),
       ('Cancer', 'Dyspnoea'),
       ('Smoker', 'Cancer')
       ]
   assert len(model.model.cpds) == 5
   assert model.model.cpds[0].variable_card == 2
   assert model.model.cpds[0].values.tolist() == [0.9, 0.1]

   assert model._add_cpd(None) is None


def test_class_BNPGM_copy(network):
   model = ProbGraphModel.read_model(network)
   model = BNPGM(network=model)

   result = model.copy()
   assert result.name == model.name
   assert result.variables == model.variables
   assert result.graph == model.graph
   assert result.potentials == model.potentials


def test_class_BNPGM_get_potential(network, capsys):
   model = ProbGraphModel.read_model(network)
   model = BNPGM(network=model)

   result = model.get_potential("None")
   captured = capsys.readouterr()
   assert captured.out == "cpd not found in model\n"
   assert result is None

   result = model.get_potential("Dyspnoea")
   assert result.variable == "Dyspnoea"
   assert result.variables[1] == "Cancer"
   assert result.values.tolist() == [[0.65, 0.3], [0.35, 0.7]]


@patch('src.pgm.bayesian_networks.DiscreteBayesianNetwork')  # Mock the DiscreteBayesianNetwork class
@patch('src.pgm.bayesian_networks.Image')  # Mock the Image class from IPython.display
@patch('src.pgm.bayesian_networks.display')  # Mock the display function
def test_class_BNPGM_draw(mock_display, mock_image, mock_DiscreteBayesianNetwork, network):
   mock_model = MagicMock()
   mock_DiscreteBayesianNetwork.return_value = mock_model
   mock_graphviz = MagicMock()
   mock_model.to_graphviz.return_value = mock_graphviz
   mock_graphviz.draw = MagicMock()

   model = ProbGraphModel.read_model(network)
   model = BNPGM(network=model)

   model.draw_graph()

   mock_model.to_graphviz.assert_called_once()
   expected_filename = "figures/Cancer model.png"
   mock_graphviz.draw.assert_called_once_with(expected_filename, prog="dot")
   
   mock_image.assert_called_once_with(expected_filename)
   mock_display.assert_called_once_with(mock_image.return_value)


def test_class_BNPGM_posterior(network):
   model = ProbGraphModel.read_model(network)
   model = BNPGM(network=model)

   model.inference()
   result = model.posterior("Xray")
   assert result.variables == ["Xray"]
   np.testing.assert_almost_equal(result.values, [0.208141, 0.791859], decimal=5)
   assert result.cardinality == 2


def test_class_BNGUM(network):
   model = ProbGraphModel.read_model(network)
   model = BNGUM(network=model)

   assert isinstance(model.model, gum.BayesNet)
   assert list(model.model.arcs()) == [(2, 3), (0, 2), (1, 2), (2, 4)]
   assert model.model.cpt("Xray").toarray().tolist() == [[0.9, 0.1], [0.2, 0.8]]

   assert model._add_cpd(None) is None


def test_class_BNGUM_copy(network):
   model = ProbGraphModel.read_model(network)
   model = BNGUM(network=model)

   result = model.copy()
   assert result.name == model.name
   assert result.variables == model.variables
   assert result.graph == model.graph
   assert result.potentials == model.potentials


def test_class_BNGUM_get_potential(network, capsys):
   model = ProbGraphModel.read_model(network)
   model = BNGUM(network=model)

   result = model.get_potential("None")
   # captured = capsys.readouterr()
   # assert captured.out == "cpd not found in model\n"
   assert result is None

   result = model.get_potential("Dyspnoea")
   assert result.variable(0).name() == "Dyspnoea"
   assert result.names[1] == "Cancer"
   assert result.toarray().tolist() == [[0.65, 0.35], [0.3, 0.7]]


@patch('src.pgm.bayesian_networks.gumimage')
@patch('src.pgm.bayesian_networks.Image')
@patch('src.pgm.bayesian_networks.display')
def test_class_BNGUM_draw(mock_display, mock_image, mock_gumimage, network):
   mock_model = MagicMock()
   mock_gumimage.return_value = mock_model

   model = ProbGraphModel.read_model(network)
   model = BNGUM(network=model)

   model.draw_graph()

   expected_filename = "figures/Cancer model.png"
   mock_gumimage.export.assert_called_once_with(model.model, expected_filename)
   
   mock_image.assert_called_once_with(expected_filename)
   mock_display.assert_called_once_with(mock_image.return_value)


def test_class_BNGUM_posterior(network):
   model = ProbGraphModel.read_model(network)
   model = BNGUM(network=model)

   model.inference()
   result = model.posterior("Xray")
   assert result.names[0] == "Xray"
   np.testing.assert_almost_equal(result.toarray(), [0.208141, 0.791859], decimal=5)
   assert result.shape == (2, )

