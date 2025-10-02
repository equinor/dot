from unittest.mock import patch, MagicMock

import pytest
import numpy as np

from src.pgm.probabilistic_graph_models import ProbGraphModel
from src.pgm.influence_diagrams import IDGUM, gum


@pytest.fixture
def network():
   data = {
      "name": "Used car buyer",
      "variables":[
         {
            "name": "Car state",
            "states": ["lemon", "peach"],
            "type": "chance",
         },
         {
            "name": "Test result",
            "states": ["no test", "lemon", "peach"],
            "type": "chance",
         },
         {
            "name": "Test decision",
            "states": ["yes", "no"],
            "type": "decision",
         },
         {
            "name": "Purchase",
            "states": ["buy without guarantee", "buy with guarantee", "don't buy"],
            "type": "decision",
         },
         {
            "name": "Testing costs",
            "states": [],
            "type": "value",
         },
         {
            "name": "Base profit",
            "states": [],
            "type": "value",
         },
         {
            "name": "Repair costs",
            "states": [],
            "type": "value",
         },
      ],
      "nodes":
      [
         "Car state",
         "Test result",
         "Test decision",
         "Purchase",
         "Testing costs",
         "Base profit",
         "Repair costs"
      ],
      "arcs":
      [
         ["Test decision", "Testing costs"],
         ["Test decision", "Test result"],
         ["Car state", "Test result"],
         ["Test result", "Purchase"],
         ["Purchase", "Base profit"],
         ["Car state", "Repair costs"],
         ["Purchase", "Repair costs"],
      ],
      "potentials": 
      [
         {
            "variable": "Car state",
            "parents": None,
            "table":
            [[0.8],
            [0.2]],
            "type": "cpd",
         },
         {
            "variable": "Test result",
            "parents": ["Car state", "Test decision"],
            "table": 
            [[1.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]],
            "type": "cpd",
         },
         {
            "variable": "Testing costs",
            "parents": ["Test decision"],
            "table": [-25, 0],
            "type": "utility",
         },
         {
            "variable": "Base profit",
            "parents": ["Purchase"],
            "table": [100, 40, 0],
            "type": "utility",
         },
         {
            "variable": "Repair costs",
            "parents": ["Car state", "Purchase"],
            "table": [[-200, 0, 0], [-40, -20, 0]],
            "type": "utility",
         },
      ]
   }
   return data


def test_class_IDGUM(network):
   model = ProbGraphModel.read_model(network)
   model = IDGUM(network=model)

   assert isinstance(model.model, gum.InfluenceDiagram)
   assert list(model.model.arcs()) == [
      (0, 1), (2, 4), (2, 1), (0, 6), (3, 6), (1, 3), (3, 5)
      ]
   assert model.model.cpt("Car state").toarray().tolist() == [0.8, 0.2]

   assert model._add_cpd(None) is None
   assert model._add_utility_table(None) is None


def test_class_IDGUM_copy(network):
   model = ProbGraphModel.read_model(network)
   model = IDGUM(network=model)

   result = model.copy()
   assert result.name == model.name
   assert result.variables == model.variables
   assert result.graph == model.graph
   assert result.potentials == model.potentials


def test_class_IDGUM_get_potential(network):
   model = ProbGraphModel.read_model(network)
   model = IDGUM(network=model)

   result = model.get_potential("None")
   assert result is None

   result = model.get_potential("Testing costs")
   assert result.variable(0).name() == "Testing costs"
   assert result.names[1] == "Test decision"
   assert result.toarray().tolist() == [[-25.0], [0.0]]


@patch('src.pgm.influence_diagrams.gumimage')
@patch('src.pgm.influence_diagrams.Image')
@patch('src.pgm.influence_diagrams.display')
def test_class_IDGUM_draw(mock_display, mock_image, mock_gumimage, network):
   mock_model = MagicMock()
   mock_gumimage.return_value = mock_model

   model = ProbGraphModel.read_model(network)
   model = IDGUM(network=model)

   model.draw_graph()

   expected_filename = "figures/Used car buyer.png" 
   mock_gumimage.export.assert_called_once_with(model.model, expected_filename)
   
   mock_image.assert_called_once_with(expected_filename)
   mock_display.assert_called_once_with(mock_image.return_value)


def test_class_IDGUM_posterior(network):
   model = ProbGraphModel.read_model(network)
   model = IDGUM(network=model)

   model.inference()
   result = model.posterior("Purchase")
   assert result.names[0] == "Purchase"
   np.testing.assert_almost_equal(result.toarray(), [0.2, 0.8, 0.0], decimal=5)
   assert result.shape == (3, )

