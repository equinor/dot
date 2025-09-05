import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.notebooks import probabilistic_graph_models as pgm


var_car_state = pgm.Variable("Car state", ["lemon", "peach"], "chance")
var_test_decision = pgm.Variable("Test decision", ["yes", "no"], "decision")
var_test_result = pgm.Variable("Test result", ["no test", "lemon", "peach"], "chance")
var_purchase = pgm.Variable("Purchase", ["buy without guarantee", "buy with guarantee", "don't buy"], "decision")
var_testing_costs = pgm.Variable("Testing costs", [], "value")
var_base_profit = pgm.Variable("Base profit", [], "value")
var_repair_costs = pgm.Variable("Repair costs", [], "value")

variables = (
    var_car_state,
    var_test_decision,
    var_test_result,
    var_purchase,
    var_testing_costs,
    var_base_profit,
    var_repair_costs,
)

node_car_state = pgm.Node("Car state")
node_test_decision = pgm.Node("Test decision")
node_test_result = pgm.Node("Test result")
node_purchase = pgm.Node("Purchase")
node_testing_costs = pgm.Node("Testing costs")
node_base_profit = pgm.Node("Base profit")
node_repair_costs = pgm.Node("Repair costs")

nodes = (
    node_car_state,
    node_test_decision,
    node_test_result,
    node_purchase,
    node_testing_costs,
    node_base_profit,
    node_repair_costs,
)

arcs = (
    pgm.Arc(node_test_decision, node_testing_costs),
    pgm.Arc(node_test_decision, node_test_result),
    pgm.Arc(node_car_state, node_test_result),
    pgm.Arc(node_test_result, node_purchase),
    pgm.Arc(node_purchase, node_base_profit),
    pgm.Arc(node_car_state, node_repair_costs),
    pgm.Arc(node_purchase, node_repair_costs),
)

graph = pgm.Graph(
    nodes,
    arcs
)

cpd_car_state = pgm.CPD(
    variable=var_car_state,
    parents=None,
    table=[[0.8], [0.2]],
    )
cpd_test_result = pgm.CPD(
    variable=var_test_result,
    parents=[var_car_state, var_test_decision],
    table=[
        [1.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0]
        ],
    )

utility_testing_costs = pgm.Utility(
    variable=var_testing_costs,
    parents=[var_test_decision],
    table=[[-25, 0]],
    )
utility_base_profit = pgm.Utility(
    variable=var_base_profit,
    parents=[var_purchase],
    table=[[100, 40, 0]],
    )
utility_repair_costs = pgm.Utility(
    variable=var_repair_costs,
    parents=[var_car_state, var_purchase],
    table=[[-200, 0, 0], [-40, -20, 0]],
    )


potentials = (
    cpd_car_state,
    cpd_test_result,
    utility_testing_costs,
    utility_base_profit,
    utility_repair_costs,
)



class UsedCarBuyerModel:
    def __init__(self):
        self.variables = variables
        self.graph = graph
        self.potentials = potentials

used_car_buyer = UsedCarBuyerModel()