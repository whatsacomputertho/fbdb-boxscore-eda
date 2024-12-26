import argparse
from typing import Type

def get_cli_args() -> Type[argparse.Namespace]:
    """
    Parse the CLI args and return as an argparse naespace

    Args:
    None

    Returns:
    argparse.Namespace: The parsed CLI args
    """
    # Initialize the parent command parser and add subparsers
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    # Initialize the boxscore subcommand parser, add subparsers
    boxscore_parser = subparsers.add_parser(
        "boxscore",
        help="Analyze historic box scores"
    )
    boxscore_subparser = boxscore_parser.add_subparsers(dest="subcommand")

    # Initialize the boxscore list subcommand parser
    boxscore_list_parser = boxscore_subparser.add_parser(
        "list",
        help="List historic box scores"
    )
    boxscore_list_parser.add_argument(
        "-y", "--year",
        dest="year",
        help="The year from which to list box scores",
        type=int,
        default=2023
    )
    boxscore_list_parser.add_argument(
        "-t", "--team",
        dest="team",
        help="The team for which to list box scores",
        type=str
    )
    boxscore_list_parser.add_argument(
        "-o", "--output",
        dest="output",
        help="The format in which to list the box scores",
        type=str,
        default="default"
    )
    boxscore_list_parser.add_argument(
        "-f", "--file",
        dest="file",
        help="The file in which to write the box scores",
        type=str
    )

    # Initialize the boxscore summarize subcommand parser
    boxscore_summarize_parser = boxscore_subparser.add_parser(
        "summarize",
        help="Summarize historic box scores"
    )
    boxscore_summarize_parser.add_argument(
        "-y", "--year",
        dest="year",
        help="The year from which to summarize box scores",
        type=int
    )
    boxscore_summarize_parser.add_argument(
        "-t", "--team",
        dest="team",
        help="The team for which to summarize box scores",
        type=str
    )
    boxscore_summarize_parser.add_argument(
        "-o", "--output",
        dest="output",
        help="The format in which to summarize the box scores",
        type=str,
        default="default"
    )
    boxscore_summarize_parser.add_argument(
        "-f", "--file",
        dest="file",
        help="The file in which to write the box score summaries",
        type=str
    )

    # Parse the CLI args and return
    return parser.parse_args()
