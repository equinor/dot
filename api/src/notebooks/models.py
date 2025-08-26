# Mimicking module calls from jupyter notebook
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.notebooks import classes


class Model:
    def __init__(self):
        self.Variable = classes.Variable
        self.Arc = classes.Arc
        self.CPD = classes.CPD
        self.PGM = classes.PGM
        self.GUM = classes.GUM


models = Model()
