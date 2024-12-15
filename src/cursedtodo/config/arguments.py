from argparse import ArgumentParser
from pathlib import Path
from dataclasses import dataclass


@dataclass
class _Arguments:
    config: Path
    verbose: bool


def _init_arg_parser() -> ArgumentParser:
    parser = ArgumentParser(description="CursedTodo")
    parser.add_argument("-c", "--config", type=Path, help="Path to the config file")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )
    return parser


def _init_arguments() -> _Arguments:
    args = _init_arg_parser().parse_args()
    return _Arguments(config=args.config, verbose=args.verbose)


Arguments = _init_arguments()

