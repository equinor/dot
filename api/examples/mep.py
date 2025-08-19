import json
import os
import sys
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import click

from src.v0.services.probability_utils.mep import common, mep, validate

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


DEFAULT_CONFIG = {
    "joint_distributions": [
        "P000",
        "P001",
        "P010",
        "P011",
        "P100",
        "P101",
        "P110",
        "P111",
    ],
    "assessments": {
        "P.01": 0.4643,
        "P.11": 0.2411,
        "P1.1": 0.3490,
        "P00.": 0.1988,
        "P01.": 0.2463,
        "P10.": 0.3017,
        "P11.": 0.2532,
    },
    "equality": [],
    "inequality": [
        "P000 <= P001",
        "P001 - P010 >= 0",
        "P011 - P010 >= 0",
        "np.mean(P) >= 0.01 ",
        "0.13 >= np.mean(P)",
    ],
    "conditioned_variables": [1, 2],
    "minimization": {
        "bounds": {
            "P000": [0.015, 1.0],
            "P001": [0.03, 1],
            "P010": [0, 1],
            "P011": [0, 1],
            "P100": [0, 0.021],
            "P101": [0, 1],
            "P110": [0, 1],
            "P111": [0, 1],
        },
        "initial_guess": {
            "P000": 0.015,
            "P001": 0.04,
            "P010": 0.01,
            "P011": 0.2,
            "P100": 0.02,
            "P101": 0.3,
            "P110": 0.2,
            "P111": 0.05,
        },
    },
}


def run(config: dict):
    common.logger.debug(f"\n{json.dumps(config, indent=2)}")
    x0 = mep.mep(config)
    common.logger.info(f"Result is {x0}")


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    "-c",
    "--config",
    type=click.Path(),
    default="-",
    help="json configuration file. Default is None for using the in-memory example",
)
def cli(config: Path | dict):
    """given a configuration, estimate probabilities by maximizing the entropy

    Example
        ```python mep.py --file <config.json>```

    The configuration file is a json file with fields

    - joint_distributions: it is a list of the probabilities to estimate.
    The probabilities are noted `Pxxx` where xxx are the indices (starting at 0)
    of the possible outcomes. E.g. P21 is the probability that the first variable
    has its 3rd outcome and the second variable has its 2nd outcomes

    - assessments: it is a dictionary of marginalization of the distributions.
    It uses the dot notation introduced by Abbas (2006). For example, P.0
    represents the marginalization over the first variable and the distribution
    when the second variable has its 1st outcomes.

    - equality: it is a list of strings representing the equality constraints
    for the optimization problem. E.g. P01 = P10

    - inequality: it is a list of strings representing the inequaility constraints
    for the optimization problem. E.g. P01 >= P10 (Be aware the strict inequality is not
    accepted)

    - conditioned_variables: it is a list of indices (starting at 0) of variables
    representing the conditioned variables when a conditional probability is
    desired. E.g. [0] for a 2 variables case means the script returns the
    probability of the first variable given the other variables

    - minimization: it is a dictionary with 2 keys

        - bounds: a dictionary giving for each desired probilities a 2 values list
    for the bounds. E.g. {"P00": [0.5, 1]} means the probability for the
    1st outcomes of both variables will be between 0.5 and 1. If the dictionary
    is empty, it assumes [0, 1] as bounds for all probabilities

        - initial_guess: a dictionary giving the initial guess for each
    probability an initial guess to start the optimization process with.
    """
    common.logger.info("Start of probability estimation by MEP")
    common.logger.debug(f" ---  {config}")

    if Path(config).is_file():
        common.logger.info(f"use file {config}")
        config_dict = validate.read_config(config)
    if config == "-":
        common.logger.info("use in memory configuration")
        config_dict = DEFAULT_CONFIG
    if not Path(config).is_file() and not config == "-":
        common.logger.info(f"Cannot interpret input file {json.dumps(config, indent=2)}")
        sys.exit()

    run(config_dict)


if __name__ == "__main__":
    cli()
