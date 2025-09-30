from itertools import product

import pyagrum as gum
from IPython.display import Image, display
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
from pgmpy.models import DiscreteBayesianNetwork
from pyagrum.lib import image as gumimage

from src.pgm import probabilistic_graph_models as pgm


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

    def copy(self):
        network = pgm.ProbGraphModel(
            name=self.name,
            variables=self.variables,
            graph=self.graph,
            potentials=self.potentials)
        return BNPGM(network=network)


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

        dims = [cpd.variable.name]
        xarr = self.potential_to_xarray(dims[0])
        if not cpd.parents:
            self.model.cpt(dims[0]).fillWith(xarr.data.tolist())
        else:
            dims += cpd.parents
            all_variables = [{cpd.variable.name: cpd.variable.states}]
            for parent in cpd.parents:
                all_variables.append({parent.name: parent.states})

            key_combinations = []
            for d in all_variables:
                key = list(d.keys())[0]
                values = list(d.values())[0]
                key_combinations.append([key])
                key_combinations.append(values)
            key_combinations = list(product(*key_combinations))

            for combination in key_combinations:
                d = {"name": combination[0]}
                d.update(
                    dict(zip(combination[2::2], combination[3::2], strict=False))
                )

                variable_name = d.pop("name")
                d_ = {self._to_valid(k): self._to_valid(v) for k,v in d.items()}
                self.model.cpt(variable_name)[d] = xarr.sel(d_).data.tolist()

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
