from itertools import product

import os
import sys

import numpy as np
import pyagrum as gum
from IPython.display import Image, display
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
from pgmpy.models import DiscreteBayesianNetwork
from pyagrum.lib import image as gumimage

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.notebooks import probabilistic_graph_models as pgm



class BNPGM(pgm.ModelABC):
    def __init__(self, *,network: pgm.ProbGraphModel):
        super().__init__(network=network)
        self.modelling()

    def modelling(self):
        self.model = DiscreteBayesianNetwork()
        self._add_arcs()
        self._add_cpds()

    def _add_arcs(self):
        for item in self.graph.arcs:
            self.model.add_edge(item.tail.id, item.head.id)

    @staticmethod
    def _add_cpd(cpd: pgm.CPD):
        if not cpd:
            return
        description = {
            "variable": cpd.variable.name,
            "variable_card": len(cpd.variable.states),
            "values": cpd.table,
        }
        if cpd.parents:
            description["evidence"] = [item.name for item in cpd.parents]
            description["evidence_card"] = tuple(
                len(item.states) for item in cpd.parents
            )
        return TabularCPD(**description)

    def _add_cpds(self):
        cpds = [BNPGM._add_cpd(item) for item in self.potentials]
        self.model.add_cpds(*cpds)

    def get_potentials(self, variable):
        found = False
        for cpd in self.potentials:
            if cpd.variable == variable:
                found = True
                print(cpd)
        if not found:
            print("cpd not found in model")

    def draw_graph(self):
        filename = f"{self.name}.png"
        viz = self.model.to_graphviz()
        viz.draw(filename, prog="dot")
        display(Image(filename))

    def inference(self, variable: str):
        ie = VariableElimination(self.model)
        return ie.query(variables=[variable])


class BNGUM(pgm.ModelABC):
    def __init__(self, *,network: pgm.ProbGraphModel):
        super().__init__(network=network)
        self.modelling()

    def modelling(self):
        self.model = gum.BayesNet()
        self._add_variables()
        self._add_arcs()
        self._add_cpds()

    def _add_variables(self):
        for variable in self.variables:
            self.model.add(
                gum.LabelizedVariable(variable.name, variable.name, variable.states)
            )

    def _add_arcs(self):
        for arc in self.graph.arcs:
            self.model.addArc(arc.tail.id, arc.head.id)

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
            # variable_names = tuple(
            #     [cpd.variable.name, *[item.name for item in cpd.parents]]
            #     )
            cpt = np.array(cpd.table).T.reshape(shape)
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

    def _add_cpds(self):
        for cpd in self.potentials:
            self._add_cpd(cpd)

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
