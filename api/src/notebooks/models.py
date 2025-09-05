# Mimicking module calls from jupyter notebook
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.notebooks import bn
from src.notebooks import id


class Model:
    def __init__(self):
        self.BNPGM = bn.BNPGM
        self.BNGUM = bn.BNGUM
        self.IDGUM = id.IDGUM

models = Model()
