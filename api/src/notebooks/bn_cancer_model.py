import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.notebooks import probabilistic_graph_models as pgm



var_pollution = pgm.Variable("Pollution", ["yes", "no"], "chance")
var_smoker = pgm.Variable("Smoker", ["yes", "no"], "chance")
var_cancer = pgm.Variable("Cancer", ["yes", "no"], "chance")
var_xray = pgm.Variable("Xray", ["yes", "no"], "chance")
var_dyspnoea = pgm.Variable("Dyspnoea", ["yes", "no"], "chance")

variables = (
    var_pollution,
    var_smoker,
    var_cancer,
    var_xray,
    var_dyspnoea,
)

node_pollution = pgm.Node("Pollution")
node_smoker = pgm.Node("Smoker")
node_cancer = pgm.Node("Cancer")
node_xray = pgm.Node("Xray")
node_dyspnoea = pgm.Node("Dyspnoea")


nodes = (
    node_pollution,
    node_smoker,
    node_cancer,
    node_xray,
    node_dyspnoea,
)

arcs = (
    pgm.Arc(node_pollution, node_cancer),
    pgm.Arc(node_smoker, node_cancer),
    pgm.Arc(node_cancer, node_xray),
    pgm.Arc(node_cancer, node_dyspnoea),
)

graph = pgm.Graph(nodes, arcs)

cpd_pollution = pgm.CPD(
    variable=var_pollution,
    parents=None,
    table=[[0.9, 0.1]],
    )
cpd_smoker = pgm.CPD(
    variable=var_smoker,
    parents=None,
    table=[[0.3], [0.7]],
    )
cpd_cancer = pgm.CPD(
    variable=var_cancer,
    parents=[var_smoker, var_pollution],
    table=[[0.03, 0.05, 0.001, 0.02], [0.97, 0.95, 0.999, 0.98]],
)
cpd_xray = pgm.CPD(
    variable=var_xray,
    parents=[var_cancer],
    table=[[0.9, 0.2], [0.1, 0.8]],
)
cpd_dyspnoea = pgm.CPD(
    variable=var_dyspnoea,
    parents=[var_cancer],
    table=[[0.65, 0.3], [0.35, 0.7]],
)

cpds = (
    cpd_pollution,
    cpd_smoker,
    cpd_cancer,
    cpd_xray,
    cpd_dyspnoea,
)


class CancerModel:
    def __init__(self):
        self.variables = variables
        self.graph = graph
        self.potentials = cpds

cancer_model = CancerModel()
