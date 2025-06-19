"""
Command-line interface for HyperEvals.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

import yaml

from . import __version__
from .eval import Eval


def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the hyperevals CLI."""
    parser = create_parser()
    parsed_args = parser.parse_args(args)

    if parsed_args.version:
        print(f"hyperevals {__version__}")
        return 0

    if not parsed_args.config:
        parser.print_help()
        return 1

    # Load config file
    config_path = Path(parsed_args.config)
    if not config_path.exists():
        print(f"Error: Config file '{config_path}' not found")
        return 1

    try:
        with open(config_path) as f:
            config = yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
        return 1

    # Run evaluation
    try:
        eval_instance = Eval(config)
        eval_instance.run()
        return 0
    except Exception as e:
        print(f"Error running evaluation: {e}")
        return 1


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        prog="hyperevals",
        description="Hyperband-optimized parallelized prompt and model parameter tuning for evaluating LLMs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  hyperevals config.yaml         # Run evaluation with config file
  hyperevals --version           # Show version information
        """,
    )

    parser.add_argument(
        "--version",
        action="store_true",
        help="Show version information and exit",
    )

    parser.add_argument(
        "config",
        nargs="?",
        help="Path to configuration file",
    )

    return parser


if __name__ == "__main__":
    sys.exit(main())
