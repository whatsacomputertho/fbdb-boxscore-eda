import argparse
from typing import Type

def set_labeled_subcommand(
        subparser: Type[argparse.ArgumentParser]
    ) -> Type[argparse.ArgumentParser]:
    """
    Adds the labeled subcommand parser & specifies its arguments

    Args:
    subparser (argparse.ArgumentParser): The subparsers on the parent parser

    Returns:
    argparse.ArgumentParser: The mutated argument parser
    """
    # Initialize the labeled subcommand parser, add subparsers
    labeled_parser = subparser.add_parser(
        "labeled",
        help="Analyze labeled box scores"
    )
    labeled_subparser = labeled_parser.add_subparsers(dest="subcommand")

    # Initialize the labeled skill-diff-scores subcommand parser
    labeled_sds_subparser = labeled_subparser.add_parser(
        "skill-diff-scores",
        help="Aggregate the scores by skill differential"
    )

    # Initialize the labeled skill-diff-scores subcommand parser
    labeled_sdsumm_subparser = labeled_subparser.add_parser(
        "skill-diff-summary",
        help="Summarize the scores by skill differential"
    )
    labeled_sdsumm_subparser.add_argument(
        "--home",
        dest="home",
        help="Whether to summarize home scores",
        action="store_true",
        default=False
    )
    labeled_sdsumm_subparser.add_argument(
        "--away",
        dest="away",
        help="Whether to summarize away scores",
        action="store_true",
        default=False
    )

    # Initialize the labeled skill-diff-visualize subcommand parser
    labeled_sdvis_subparser = labeled_subparser.add_parser(
        "skill-diff-visualize",
        help="Visualize the scoring by skill differential"
    )
    labeled_sdvis_subparser.add_argument(
        "--home",
        dest="home",
        help="Whether to visualize home scores only",
        action="store_true",
        default=False
    )
    labeled_sdvis_subparser.add_argument(
        "--away",
        dest="away",
        help="Whether to visualize away scores only",
        action="store_true",
        default=False
    )

    # Initialize the labeled home-away-visualize subcommand parser
    labeled_home_away_subparser = labeled_subparser.add_parser(
        "home-away-visualize",
        help="Visualize the scoring by home versus away"
    )

    # Initialize the labeled mean-score-train subcommand parser
    mean_model_subparser = labeled_subparser.add_parser(
        "mean-score-train",
        help="Train a regression model for mean score"
    )
    mean_model_subparser.add_argument(
        "--away",
        dest="away",
        help="Whether to train using away scores only",
        action="store_true",
        default=False
    )

    # Initialize the labeled std-score-train subcommand parser
    std_model_subparser = labeled_subparser.add_parser(
        "std-score-train",
        help="Train a regression model for std score"
    )
    std_model_subparser.add_argument(
        "--away",
        dest="away",
        help="Whether to train using away scores only",
        action="store_true",
        default=False
    )
    return subparser

def set_boxscore_subcommand(
        subparser: Type[argparse.ArgumentParser]
    ) -> Type[argparse.ArgumentParser]:
    """
    Adds the boxscore subcommand parser & specifies its arguments

    Args:
    subparser (argparse.ArgumentParser): The subparsers on the parent parser

    Returns:
    argparse.ArgumentParser: The mutated argument parser
    """
    # Initialize the boxscore subcommand parser, add subparsers
    boxscore_parser = subparser.add_parser(
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
        "--offense",
        dest="offense",
        help="Whether to summarize only offense",
        action="store_true",
        default=False
    )
    boxscore_summarize_parser.add_argument(
        "--defense",
        dest="defense",
        help="Whether to summarize only defense",
        action="store_true",
        default=False
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

    # Initialize the boxscore visualize subcommand parser
    boxscore_visualize_parser = boxscore_subparser.add_parser(
        "visualize",
        help="Visualize historic box scores"
    )
    boxscore_visualize_parser.add_argument(
        "--offense",
        dest="offense",
        help="Whether to visualize historic offensive box scores",
        action="store_true",
        default=False
    )
    boxscore_visualize_parser.add_argument(
        "--defense",
        dest="defense",
        help="Whether to visualize historic defensive box scores",
        action="store_true",
        default=False
    )

    # Initialize the boxscore label subcommand parser
    boxscore_label_parser = boxscore_subparser.add_parser(
        "label",
        help="Label historic box scores"
    )

    # Initialize the boxscore aggregate subcommand parser
    boxscore_aggregate_parser = boxscore_subparser.add_parser(
        "aggregate",
        help="Aggregate labeled historic box scores"
    )

    # Initialize the boxscore frequency subcommand parser
    boxscore_frequency_parser = boxscore_subparser.add_parser(
        "frequency",
        help="Get the frequency of historic box scores"
    )

    # Initialize the boxscore model-frequency subcommand parser
    boxscore_model_frequency_parser = boxscore_subparser.add_parser(
        "model-frequency",
        help="Get the frequency of model-generated box scores"
    )

    # Initialize the boxscore model-frequency subcommand parser
    boxscore_model_frequency_mse_parser = boxscore_subparser.add_parser(
        "model-frequency-mse",
        help="Get the mean squared error of model-generated versus real box scores"
    )

    # Initialize the boxscore tie-frequency subcommand parser
    boxscore_tie_frequency_parser = boxscore_subparser.add_parser(
        "tie-frequency",
        help="Get the frequency of historic ties"
    )

    # Initialize the boxscore tie-frequency-by-skill subcommand parser
    boxscore_tie_frequency_by_skill_parser = boxscore_subparser.add_parser(
        "tie-frequency-by-skill",
        help="Get the frequency of historic ties"
    )
    return subparser

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

    # Add the boxscore subcommand to the parent parser
    subparsers = set_boxscore_subcommand(subparsers)
    subparsers = set_labeled_subcommand(subparsers)

    # Parse the CLI args and return
    return parser.parse_args()
