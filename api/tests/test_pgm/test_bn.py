from unittest.mock import patch, mock_open
import json

import pytest
import numpy as np

from src.pgm.probabilistic_graph_models import ProbGraphModel, ModelABC
from src.pgm.bn import BNPGM, DiscreteBayesianNetwork, BNGUM

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


def test_class_BNPGM_get_potentials(network):
   model = ProbGraphModel.read_model(network)
   model = BNPGM(network=model)

# get_potentials(self, variable):



#     def get_potentials(self, variable):
#         found = False
#         for cpd in self.potentials:
#             if cpd.variable == variable:
#                 found = True
#                 print(cpd)
#         if not found:
#             print("cpd not found in model")

#     def draw_graph(self):
#         filename = f"{self.name}.png"
#         viz = self.model.to_graphviz()
#         viz.draw(filename, prog="dot")
#         display(Image(filename))

#     def inference(self, variable: str):
#         ie = VariableElimination(self.model)
#         return ie.query(variables=[variable])


# class BNGUM(pgm.ModelABC):
#     def __init__(self, *,network: pgm.ProbGraphModel):
#         super().__init__(network=network)
#         self.modelling()

#     def modelling(self):
#         self.model = gum.BayesNet()
#         self._add_variables()
#         self._add_arcs()
#         self._add_cpds()

#     def _add_variables(self):
#         for variable in self.variables:
#             self.model.add(
#                 gum.LabelizedVariable(variable.name, variable.name, variable.states)
#             )

#     def _add_arcs(self):
#         for arc in self.graph.arcs:
#             self.model.addArc(arc.tail.id, arc.head.id)

#     def _add_cpd(self, cpd):
#         if not cpd:
#             return

#         dims = [cpd.variable.name]
#         xarr = self.potential_to_xarray(dims[0])
#         if not cpd.parents:
#             self.model.cpt(dims[0]).fillWith(xarr.data.tolist())
#         else:
#             dims += cpd.parents
#             all_variables = [{cpd.variable.name: cpd.variable.states}]
#             for parent in cpd.parents:
#                 all_variables.append({parent.name: parent.states})

#             key_combinations = []
#             for d in all_variables:
#                 key = list(d.keys())[0]
#                 values = list(d.values())[0]
#                 key_combinations.append([key])
#                 key_combinations.append(values)
#             key_combinations = list(product(*key_combinations))

#             for combination in key_combinations:
#                 d = {"name": combination[0]}
#                 d.update(
#                     dict(zip(combination[2::2], combination[3::2], strict=False))
#                 )

#                 variable_name = d.pop("name")
#                 d_ = {self._to_valid(k): self._to_valid(v) for k,v in d.items()}
#                 self.model.cpt(variable_name)[d] = xarr.sel(d_).data.tolist()

#     def _add_cpds(self):
#         for cpd in self.potentials:
#             self._add_cpd(cpd)

#     def get_potentials(self, variable):
#         if variable not in [item.name for item in self.variables]:
#             print("cpd not found in model")
#             return
#         print(self.model.cpt(variable))

#     def draw_graph(self):
#         filename = f"{self.name}.png"
#         gumimage.export(self.model, filename)
#         display(Image(filename))

#     def inference(self, variable: str):
#         ie = gum.LazyPropagation(self.model)
#         ie.makeInference()
#         return ie.posterior(variable)
