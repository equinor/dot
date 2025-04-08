"""
Conversion of influence diagram to pyAgrum format.

.. seealso:
    pyAgrum documentation https://pyagrum.readthedocs.io/
"""

from itertools import product

import pyAgrum as gum

from src.v0.services.classes.discrete_conditional_probability import (
    DiscreteConditionalProbability,
)
from src.v0.services.classes.discrete_unconditional_probability import (
    DiscreteUnconditionalProbability,
)
from src.v0.services.classes.influence_diagram import InfluenceDiagram
from src.v0.services.classes.node import (
    DecisionNode,
    UncertaintyNode,
    UtilityNode,
)
from src.v0.services.errors import (
    ArcPyAgrumFormatError,
    InfluenceDiagramNotAcyclicError,
    ProbabilityPyAgrumFormatError,
)


class InfluenceDiagramToPyAgrum:
    def probabilities_conversion(self, probability):
        if isinstance(probability, DiscreteConditionalProbability):
            return self.conditional_probabilities_conversion(probability)
        if isinstance(probability, DiscreteUnconditionalProbability):
            return self.unconditional_probabilities_conversion(probability)

    def unconditional_probabilities_conversion(self, probability):
        variables = probability.variables
        if len(variables) != 1:
            raise ProbabilityPyAgrumFormatError(variables)
        return [
            (
                {},
                [
                    probability._cpt.sel(**{variables[0]: state})
                    for state in probability.outcomes
                ],
            )
        ]

    def conditional_probabilities_conversion(self, probability):
        # agrum = list()
        coords = probability._cpt.coords
        variables = {
            key: coords[key].data.tolist() for key in coords if key is not coords.dims[0]
        }
        agrum_dict = {k: list(range(len(v))) for k, v in variables.items()}
        agrum_dict = [
            dict(zip(agrum_dict.keys(), values, strict=False))
            for values in product(*agrum_dict.values())
        ]
        agrum_prob = [
            probability.get_distribution(
                **{key: coords[key][val] for key, val in item.items()}
            ).data.tolist()
            for item in agrum_dict
        ]
        agrum = list(zip(agrum_dict, agrum_prob, strict=False))
        return agrum

    def nodes_conversion(self, nodes, gum_id):
        # create an uuid for gum as 8 bytes integer and keep relation to uuid
        uuid_dot_to_gum = {}
        uuid_gum_to_dot = {}
        node_uuid = {}

        for node in nodes:
            labelized_variables = [node.shortname, node.description]
            if isinstance(node, UncertaintyNode):
                try:
                    labelized_variables.append(node.outcomes)
                    variable_id = gum_id.addChanceNode(
                        gum.LabelizedVariable(*labelized_variables)
                    )
                except Exception as e:
                    raise ProbabilityPyAgrumFormatError(e)
            elif isinstance(node, DecisionNode):
                # This works even when alternatives are [""] or None
                labelized_variables.append(node.alternatives)
                variable_id = gum_id.addDecisionNode(
                    gum.LabelizedVariable(*labelized_variables)
                )
            elif isinstance(node, UtilityNode):
                # Utility not yet implemented
                labelized_variables.append(1)
                variable_id = gum_id.addUtilityNode(
                    gum.LabelizedVariable(*labelized_variables)
                )

            uuid_dot_to_gum[node.uuid] = variable_id
            uuid_gum_to_dot[variable_id] = node.uuid
            node_uuid[variable_id] = node

        return uuid_dot_to_gum, uuid_gum_to_dot, node_uuid

    def arcs_conversion(self, arcs, gum_id, uuid_dot_to_gum):
        for arc in arcs:
            tail = uuid_dot_to_gum[arc.tail.uuid]
            head = uuid_dot_to_gum[arc.head.uuid]
            try:
                gum_id.addArc(tail, head)
            except Exception as e:
                raise ArcPyAgrumFormatError(e)
        return None

    def conversion(self, influence_diagram: InfluenceDiagram):
        if not influence_diagram.is_acyclic:
            raise InfluenceDiagramNotAcyclicError(False)

        gum_id = gum.InfluenceDiagram()
        variable_id = []

        uuid_dot_to_gum, uuid_gum_to_dot, node_uuid = self.nodes_conversion(
            influence_diagram.nodes, gum_id
        )
        # Add head and tail in gum_id
        self.arcs_conversion(influence_diagram.arcs, gum_id, uuid_dot_to_gum)

        for variable_id in uuid_gum_to_dot:
            if isinstance(node_uuid[variable_id], UncertaintyNode):
                for agrum_prob in self.probabilities_conversion(
                    node_uuid[variable_id].probability
                ):
                    gum_id.cpt(variable_id)[agrum_prob[0]] = agrum_prob[1]

        return gum_id
