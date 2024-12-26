import argparse
import json
import matplotlib.pyplot
import os
import pandas
from boxscore.boxscore import BoxScoreList, BoxScoreSeason, BoxScoreSummaryList
from cli.cli import get_cli_args

def list_boxscores(args: argparse.Namespace) -> None:
    """
    Execute the boxscore list CLI command

    Args:
    args (argparse.Namespace): The CLI args

    Returns:
    None
    """
    # Load the year of scores
    with open(f"./data/raw/{args.year}.json") as data:
        scores = BoxScoreList(json.load(data))

    # Filter a team's scores if a team is given
    filtered = scores
    if args.team is not None:
        filtered = scores.to_box_score_season().get_team_box_scores(args.team)

    # Get the box scores as a string
    box_score_str = ""
    if args.output == "default":
        box_score_str = str(filtered)
    elif args.output == "json":
        box_score_str = json.dumps(filtered, indent=4)
    elif args.output == "table":
        box_score_str = pandas.read_json(json.dumps(filtered)).to_string()
    else:
        raise Exception(f"Unrecognized output format {args.output}")

    # Output the box scores either to stdout or to a file
    if args.file is not None:
        with open(args.file, 'w') as out:
            out.write(box_score_str)
    else:
        print(box_score_str)

def summarize_boxscores(args: argparse.Namespace) -> None:
    """
    Execute the boxscore summarize CLI command

    Args:
    args (argparse.Namespace): The CLI args

    Returns:
    None
    """
    # Load each year of box scores, or load a specific year if a year is given
    years = [
        int(d.replace(".json", "")) for d in os.listdir("./data/raw")
    ]
    if args.year is not None:
        years = [ args.year ]
    
    # Summarize each year and add each summary to a BoxScoreSummaryList
    summary_list = BoxScoreSummaryList()
    for year in years:
        # Load the year of scores
        with open(f"./data/raw/{year}.json") as data:
            scores = BoxScoreList(json.load(data))

        # Filter a team's scores if a team is given
        # Summarize and add to the summary list
        season_scores = scores.to_box_score_season(year)
        if args.team is not None:
            season_scores = season_scores.get_team_box_scores(args.team)
            summary_list.add_summary(
                season_scores.summarize_team_scores(args.team)
            )
        else:
            summary_list.add_summaries(season_scores.summarize())

    # Get the summaries as a string
    summary_str = ""
    if args.output == "default":
        summary_str = str(summary_list)
    elif args.output == "json":
        summary_str = json.dumps(summary_list, indent=4)
    elif args.output == "table":
        summary_str = pandas.read_json(
            json.dumps(summary_list)
        ).to_string()
    else:
        raise Exception(f"Unrecognized output format {args.output}")

    # Output the box scores either to stdout or to a file
    if args.file is not None:
        with open(args.file, 'w') as out:
            out.write(summary_str)
    else:
        print(summary_str)

def main(args: argparse.Namespace) -> None:
    """
    Execute the football database box score EDA CLI

    Args:
    args (argparse.Namespace): The CLI args

    Returns:
    None
    """
    # Determine which command and subcommand was executed
    if args.command == "boxscore":
        if args.subcommand == "list":
            list_boxscores(args)
        elif args.subcommand == "summarize":
            summarize_boxscores(args)
        else:
            raise Exception(
                f"Unrecognized boxscore subcommand {args.subcommand}"
            )
    else:
        raise Exception(
            f"Unrecognized command {args.command}"
        )

if __name__ == "__main__":
    main(get_cli_args())

# Parse the data into a dataframe
#df = pandas.read_json("./data/raw/2023.json")

#print(df.to_string())
