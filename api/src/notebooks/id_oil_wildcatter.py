import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.notebooks import probabilistic_graph_models as pgm

var_oil_content = pgm.Variable("Oil content", ["dry", "wet", "soaking"], "chance")
var_test_decision = pgm.Variable("Test decision", ["yes", "no"], "decision")
var_test_result = pgm.Variable("Test result", ["closed", "open", "diffuse"], "chance")
var_drilling = pgm.Variable("Drilling", ["yes", "no"], "decision")
var_testing_costs = pgm.Variable("Testing costs", [], "value")
var_reward = pgm.Variable("Reward", [], "value")

variables = (
    var_oil_content,
    var_test_decision,
    var_test_result,
    var_drilling,
    var_testing_costs,
    var_reward,
)

node_oil_content = pgm.Node("Oil content")
node_test_decision = pgm.Node("Test decision")
node_test_result = pgm.Node("Test result")
node_drilling = pgm.Node("Drilling")
node_testing_costs = pgm.Node("Testing costs")
node_reward = pgm.Node("Reward")

nodes = (
    node_oil_content,
    node_test_decision,
    node_test_result,
    node_drilling,
    node_testing_costs,
    node_reward,
)

arcs = (
    pgm.Arc(node_test_decision, node_testing_costs),
    pgm.Arc(node_test_decision, node_test_result),
    pgm.Arc(node_test_decision, node_drilling),
    pgm.Arc(node_oil_content, node_test_result),
    pgm.Arc(node_oil_content, node_reward),
    pgm.Arc(node_test_result, node_drilling),
    pgm.Arc(node_drilling, node_reward),
)

graph = pgm.Graph(
    nodes,
    arcs
)

cpd_oil_content = pgm.CPD(
    variable=var_oil_content,
    parents=None,
    table=[[0.5], [0.3], [0.2]],
    )
cpd_test_result = pgm.CPD(
    variable=var_test_result,
    parents=[var_test_decision, var_oil_content],
    table=[
		[0.1, 0.3, 0.5, 0.333333, 0.333333, 0.333333],
		[0.3, 0.4, 0.4, 0.333333, 0.333333, 0.333333],
		[0.6, 0.3, 0.1, 0.333333, 0.333333, 0.333333]
        ],
    )


utility_testing_costs = pgm.Utility(
    variable=var_testing_costs,
    parents=[var_test_decision],
    table=[[-10, 0]],
    )
utility_reward = pgm.Utility(
    variable=var_reward,
    parents=[var_drilling, var_oil_content],
    table=[[-70, 50, 200, 0, 0, 0]],
    )


potentials = (
    cpd_oil_content,
    cpd_test_result,
    utility_testing_costs,
    utility_reward,
)



class OilWildcatterModel:
    def __init__(self):
        self.variables = variables
        self.graph = graph
        self.potentials = potentials

oil_wildcatter = OilWildcatterModel()
