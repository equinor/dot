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
