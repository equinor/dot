from itertools import product

import pyagrum as gum
from IPython.display import Image, display
from pyagrum.lib import image as gumimage

from src.pgm import probabilistic_graph_models as pgm


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

    def copy(self):
        network = pgm.ProbGraphModel(
            name=self.name,
            variables=self.variables,
            graph=self.graph,
            potentials=self.potentials)
        return IDGUM(network=network)
    
    def _add_potential(self, potential):
        if isinstance(potential, pgm.CPD):
            print("CPD")
            print(potential.variable.name)
            self._add_cpd(potential)
        if isinstance(potential, pgm.Utility):
            print("Utility")
            print(potential.variable.name)
            self._add_utility_table(potential)

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

    def _add_utility_table(self, utility):
        if not utility:
            return

        xarr = self.potential_to_xarray(utility.variable.name)
        all_variables = [{parent.name: parent.states} for parent in utility.parents]
        key_combinations = []
        for d in all_variables:
            key = list(d.keys())[0]
            values = list(d.values())[0]
            key_combinations.append([key])
            key_combinations.append(values)
        key_combinations = list(product(*key_combinations))

        for combination in key_combinations:
            d = dict(zip(combination[0::2], combination[1::2], strict=False))
            d_ = {self._to_valid(k): self._to_valid(v) for k,v in d.items()}
            self.model.utility(utility.variable.name)[d] = xarr.sel(d_).data.tolist()

    def _add_potentials(self):
        for potential in self.potentials:
            self._add_potential(potential)

    def get_potential(self, variable):
        if variable not in [item.name for item in self.variables]:
            print("potential not found in model")
            return
        var = self.get_variable_by_name(variable)
        potential_type = "cpt" if var.type == "chance" else "utility"
        return getattr(self.model, potential_type)(variable)

    def draw_graph(self):
        filename = f"figures/{self.name}.png"
        gumimage.export(self.model, filename)
        display(Image(filename))

    def inference(self):
        ie = gum.ShaferShenoyLIMIDInference(self.model)
        ie.makeInference()
        self.ie = ie
    
    def posterior(self, variable: str):
        return self.ie.posterior(variable)
