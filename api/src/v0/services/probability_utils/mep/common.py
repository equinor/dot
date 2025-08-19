import logging  # use a local logger as the logging of the api needs to be revisited
from collections import namedtuple

logging.basicConfig(
    format="[%(asctime)s - %(funcName)s():%(lineno)s] %(levelname)s: %(message)s"
)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

Configuration = namedtuple(
    "Configuration",
    [
        "joint_distributions",
        "assessments",
        "equality",
        "inequality",
        "conditioned_variables",
        "minimization",
    ],
)
Minimization = namedtuple("minimization", ["initial_guess", "bounds"])

PROBABILITY_TAG = "P"
