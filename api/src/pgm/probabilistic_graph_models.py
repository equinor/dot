import re
from abc import ABC, abstractmethod
from collections import namedtuple

import numpy as np
import xarray as xr

Variable = namedtuple("Variable", ["name", "states", "type"])
Node = namedtuple("Node", ["id"])
Arc = namedtuple("Arc", ["tail", "head"])
Graph = namedtuple("Graph", ["nodes", "arcs"])
CPD = namedtuple(
    "CPD",
    [
        "variable",
        "parents",
        "table",
    ],
)
Utility = namedtuple(
    "Utility",
    [
        "variable",
        "parents",
        "table"
    ],
)


class ProbGraphModel:
    def __init__(self,
                 *,
                 name: str,
                 variables: tuple[Variable],
                 graph: Graph,
                 potentials: tuple[CPD | Utility],
                 ):
        self.name = name
        self.variables = variables
        self.graph = graph
        self.potentials = potentials

    def print_variables(self):
        print("Variables:")
        print(*self.variables, sep="\n")
        print("\n")

    def print_nodes(self):
        print("Nodes:")
        print(*[item.id for item in self.graph.nodes], sep="\n")
        print("\n")

    def print_arcs(self):
        print("Arcs:")
        print(*[(item.tail.id, item.head.id) for item in self.graph.arcs], sep="\n")
        print("\n")

    def print_potentials(self):
        print("Potentials:")
        print(*self.potentials, sep="\n")
        print("\n")

    def get_potential_by_name(self, name: str):
        potential = [p for p in self.potentials  if p.variable.name == name]
        if potential:
            return potential[0]
        else:
            return

    def get_variable_by_name(self, name: str):
        variable = [v for v in self.variables if v.name == name]
        if variable:
            return variable[0]
        else:
            return None

    @staticmethod
    def _to_valid(s: str):
        return re.sub(r'\W+|^(?=\d)','_', s)

    def potential_to_xarray(self, name):
        potential = self.get_potential_by_name(name)
        variables = []
        if potential.variable.states:
            variables += [potential.variable]
        if potential.parents:
            variables += potential.parents
        dims = [self._to_valid(item.name) for item in variables if item]
        coords = {self._to_valid(item.name): [self._to_valid(s) for s in item.states] \
                  for item in variables if item}
        shape = tuple(len(item) for item in coords.values())
        table = np.array(potential.table).reshape(shape)
        return xr.DataArray(table, dims=dims, coords=coords)


class ModelABC(ABC, ProbGraphModel):
    def __init__(self, *,network: ProbGraphModel):
        ProbGraphModel.__init__(
            self,
            name=network.name,
            variables=network.variables,
            graph=network.graph,
            potentials=network.potentials
        )
        self.model = None

    @abstractmethod
    def modelling(self):
        raise NotImplementedError

    @abstractmethod
    def copy(self, dst):
        raise NotImplementedError

    @abstractmethod
    def get_potentials(self, variable: str):
        raise NotImplementedError

    @abstractmethod
    def draw_graph(self):
        raise NotImplementedError

    @abstractmethod
    def inference(self, variable: str):
        raise NotImplementedError



# def id_to_bn(id, name):
#     nodes = [item.name for item in id.variables]
#     print(nodes)
#     print(id.variables)
#     bn_variables = _id_to_bn_variables(id.variables)
#     bn_arcs = _id_to_bn_arcs(bn_variables, id.arcs)
#     bn_potentials = _id_to_bn_potentials(
#         id.variables,
#         id.potentials,
#         bn_variables,
#         bn_arcs,
#         )
#     return ProbGraphModel(
#         name=name,
#         vcariables=bn_variables,
#         graph=bn_graph,
#         potentials=bn_potentials)


#     return bn_variables, bn_arcs, bn_potentials






# def get_variable_by_name(name, variables):
#     variable = [variable_ for variable_ in variables if variable_.name == name]
#     if variable:
#         return variable[0]
#     else:
#         return None


# def _id_to_bn_variables(variables):
#     bn_variables = tuple(
#         Variable(item.name, ["true", "false"], "chance") \
#             if item.type == "value" else \
#                 Variable(item.name, item.states, "chance") \
#                     for item in variables
#                 )
#     return bn_variables


# def _id_to_bn_arcs(bn_variables, arcs):
#     return tuple(
#         Arc(
#             get_variable_by_name(tail.name, bn_variables),
#             get_variable_by_name(head.name, bn_variables)
#             ) \
#                 for (tail, head) in arcs
#                 )


# def _id_to_bn_chance_potential(potential, bn_variables):
#     bn_variable = get_variable_by_name(potential.variable.name, bn_variables)
#     bn_parents = [] if not potential.parents \
#         else [
#             get_variable_by_name(parent.name, bn_variables) \
#                 for parent in potential.parents
#             ]
#     bn_table = potential.table
#     return CPD(
#         bn_variable,
#         bn_parents,
#         bn_table,
#     )


# def _id_to_bn_decision_potential(variable, bn_variables, bn_arcs):
#     bn_variable = get_variable_by_name(variable.name, bn_variables)
#     states_count = len(bn_variable.states)
#     bn_parents = [arc.tail for arc in bn_arcs if arc.head == bn_variable]
#     shape = (states_count,) if not bn_parents \
#         else (states_count, *(len(item.states) for item in bn_parents))
#     bn_table = np.ones(shape)
#     bn_table /= bn_table.size
#     bn_table.reshape((states_count, -1))
#     return CPD(
#         bn_variable,
#         bn_parents,
#         bn_table.tolist()
#     )

# def _id_to_bn_value_potential(potential, bn_variables):
#     bn_variable = get_variable_by_name(potential.variable.name, bn_variables)
#     probability_true = np.empty(tuple(len(parent.states) for parent in potential.parents))
#     probability_false = 1.0 - probability_true
#     print(" 00000 ", probability_true, probability_false)

#     bn_parents = [] if not potential.parents \
#         else [
#             get_variable_by_name(parent.name, bn_variables) \
#                 for parent in potential.parents
#             ]

#     bn_table = [[probability_true, probability_false]]

#     return CPD(
#         bn_variable,
#         bn_parents,
#         bn_table,
#     )


# def _potential_from_variable(variable, potentials):
#     potential = [item for item in potentials  if item.variable == variable]
#     if potential:
#         return potential[0]
#     else:
#         return


# def _id_to_bn_potentials(
#         id_variables,
#         id_potentials,
#         bn_variables,
#         bn_arcs,
#         ):
#     bn_cpds = []
#     for id_variable in id_variables:
#         print(" --- ", id_variable.name, id_variable.type)
#         id_potential = _potential_from_variable(id_variable, id_potentials)

#         if id_variable.type == "decision":
#             bn_cpds.append(
#                 _id_to_bn_decision_potential(id_variable, bn_variables, bn_arcs)
#                 )
#             continue

#         if id_variable.type == "chance":
#             bn_cpds.append(_id_to_bn_chance_potential(id_potential, bn_variables))
#             continue

#         if id_variable.type == "value":
#             bn_cpds.append(_id_to_bn_value_potential(id_potential, bn_variables))
#             continue
#     print(bn_cpds)


# def id_to_bn(variables, arcs, potentials):
#     nodes = [item.name for item in variables]
#     print(nodes)
#     print(variables)
#     bn_variables = _id_to_bn_variables(variables)
#     bn_arcs = _id_to_bn_arcs(bn_variables, arcs)
#     bn_potentials = _id_to_bn_potentials(
#         variables,
#         potentials,
#         bn_variables,
#         bn_arcs,
#         )
#     return bn_variables, bn_arcs, bn_potentials
