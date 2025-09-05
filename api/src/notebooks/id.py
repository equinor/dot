from itertools import product

import os
import sys

import numpy as np
import pyagrum as gum
from IPython.display import Image, display
from pyagrum.lib import image as gumimage

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.notebooks import probabilistic_graph_models as pgm



class IDGUM(pgm.ModelABC):
    def __init__(self, *,network: pgm.ProbGraphModel):
        super().__init__(network=network)
        self.modelling()

    def modelling(self):
        self.model = gum.InfluenceDiagram()
        self._add_variables()
        self._add_arcs()
        self._add_potentials()

    def _add_variables(self):
        for variable in self.variables:
            if variable.type == "chance":
                self.model.addChanceNode(
                    gum.LabelizedVariable(variable.name, variable.name, variable.states)
                    )
            if variable.type == "decision":
                self.model.addDecisionNode(
                    gum.LabelizedVariable(variable.name, variable.name, variable.states)
                    )
            if variable.type == "value":
                self.model.addUtilityNode(
                    gum.LabelizedVariable(variable.name, variable.name, 1)
                )

    def _add_arcs(self):
        for arc in self.graph.arcs:
            self.model.addArc(arc.tail.id, arc.head.id)

    def _add_potential(self, potential):
        if isinstance(potential, pgm.CPD):
            print(potential.variable.name)
            self._add_cpd(potential)
        if isinstance(potential, pgm.Utility):
            print("Utility")
        if not isinstance(potential, pgm.CPD) and not isinstance(potential, pgm.Utility):
            print("Unknonw")

    def _add_cpd(self, cpd):
        if not cpd:
            return

        if not cpd.parents:
            shape = (len(cpd.variable.states),)
            cpt = np.array(cpd.table).T.reshape(shape)
            self.model.cpt(cpd.variable.name).fillWith(cpt.tolist())
        else:
            shape = (
                len(cpd.variable.states),
                *tuple(len(item.states) for item in cpd.parents),
            )
            cpt = np.array(cpd.table).reshape(shape)
            all_variables = [{cpd.variable.name: cpd.variable.states}]
            for parent in cpd.parents:
                all_variables.append({parent.name: parent.states})
            key_combinations = []
            ind_combinations = []

            for k, d in enumerate(all_variables):
                key = list(d.keys())[0]
                values = list(d.values())[0]
                key_combinations.append([key])
                key_combinations.append(values)
                ind_combinations.append([k])
                ind_combinations.append(list(range(len(values))))
            key_combinations = list(product(*key_combinations))
            ind_combinations = list(product(*ind_combinations))

            for combination in zip(key_combinations, ind_combinations, strict=False):
                d = {"name": combination[0][0]}
                d.update(
                    dict(zip(combination[0][2::2], combination[0][3::2], strict=False))
                )
                ind = combination[1][3::2]

                variable_name = d.pop("name")
                self.model.cpt(variable_name)[d] = cpt[:, *ind].tolist()

    def _add_potentials(self):
        for potential in self.potentials:
            self._add_potential(potential)

    def get_potentials(self, variable):
        if variable not in [item.name for item in self.variables]:
            print("cpd not found in model")
            return
        print(self.model.cpt(variable))

    def draw_graph(self):
        filename = f"{self.name}.png"
        gumimage.export(self.model, filename)
        display(Image(filename))

    def inference(self, variable: str):
        ie = gum.LazyPropagation(self.model)
        ie.makeInference()
        return ie.posterior(variable)
