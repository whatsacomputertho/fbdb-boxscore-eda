import argparse
import json
import matplotlib.pyplot
import os
import pandas
import random
from boxscore.boxscore  import  BoxScoreList, \
                                BoxScoreSummaryList, \
                                LabeledBoxScore
from sklearn.cluster    import  KMeans

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
            team_summary = season_scores.summarize_team_scores(args.team)
            team_summary.team = f"{year} {args.team}"
            summary_list.add_summary(team_summary)
        else:
            summary_list.add_summaries(season_scores.summarize())
    
    # Summarize only offense or defense if requested
    if args.offense:
        summary_list = summary_list.get_offense_summary_json()
    elif args.defense:
        summary_list = summary_list.get_defense_summary_json()

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

def visualize_boxscores(args: argparse.Namespace) -> None:
    """
    Execute the boxscore visualize subcommand

    Args:
    args (argparse.Namespace): The CLI args

    Returns:
    None
    """
    # Initialize a pyplot figure
    fig, ax = matplotlib.pyplot.subplots()

    # Initialize the dataframe
    if args.offense:
        # Sort and filter the dataframe
        dataframe = pandas.read_json("./data/preprocessed/offense.json")
        dataframe = dataframe.sort_values(["mean", "std"], ascending=False)
        dataframe = dataframe.query('count > 5')
        dataframe = dataframe.dropna()
        
        # Set the figure title & y-axis label
        matplotlib.pyplot.title('Historic football offense summary data')
        ax.set_xlabel('Mean points for')
        ax.set_ylabel('Median points for')
    elif args.defense:
        # Sort and filter the dataframe
        dataframe = pandas.read_json("./data/preprocessed/defense.json")
        dataframe = dataframe.sort_values(["mean", "std"])
        dataframe = dataframe.query('count > 5')
        dataframe = dataframe.dropna()
        
        # Set the figure title
        matplotlib.pyplot.title('Historic football defense summary data')
        ax.set_xlabel('Mean points against')
        ax.set_ylabel('Median points against')
    else:
        raise Exception("Must provide either --offense or --defense")

    # Plot the dataframe
    filtered = dataframe[["mean", "50%"]]
    kmeans = KMeans(n_clusters=5)
    kmeans.fit(filtered)
    filtered['cluster'] = kmeans.labels_

    # Visualize the clusters
    matplotlib.pyplot.scatter(filtered['mean'], filtered['50%'], c=filtered['cluster'])
    matplotlib.pyplot.show()

def label_boxscores(args: argparse.Namespace) -> None:
    """
    Execute the boxscore label subcommand

    Args:
    args (argparse.Namespace): The CLI args

    Returns:
    None
    """
    # Initialize the offense & defense dataframes
    offense_dataframe = pandas.read_json("./data/preprocessed/offense.json")
    offense_dataframe = offense_dataframe.sort_values(["mean", "std"], ascending=True)
    offense_dataframe = offense_dataframe.query('count > 5')
    offense_dataframe = offense_dataframe.dropna()
    defense_dataframe = pandas.read_json("./data/preprocessed/defense.json")
    defense_dataframe = defense_dataframe.sort_values(["mean", "std"], ascending=False)
    defense_dataframe = defense_dataframe.query('count > 5')
    defense_dataframe = defense_dataframe.dropna()

    # Cluster each using k-means clustering
    offense_filtered = offense_dataframe[["mean", "50%"]]
    offense_kmeans = KMeans(n_clusters=5)
    offense_kmeans.fit(offense_filtered)
    offense_dataframe['offense_overall'] = offense_kmeans.labels_
    offense_dataframe['offense_overall'] = pandas.factorize(
        offense_dataframe['offense_overall']
    )[0] + 1
    defense_filtered = defense_dataframe[["mean", "50%"]]
    defense_kmeans = KMeans(n_clusters=5)
    defense_kmeans.fit(defense_filtered)
    defense_dataframe['defense_overall'] = defense_kmeans.labels_
    defense_dataframe['defense_overall'] = pandas.factorize(
        defense_dataframe['defense_overall']
    )[0] + 1

    # Sort by team name for labelling
    offense_dataframe.sort_values("team")
    defense_dataframe.sort_values("team")

    # Loop through each year
    years = [
        int(d.replace(".json", "")) for d in os.listdir("./data/raw")
    ]
    for year in years:
        print(f"Labelling year {year}")
        labeled = []

        # Load the year of scores
        with open(f"./data/raw/{year}.json") as data:
            scores = BoxScoreList(json.load(data))
        
        # For each box score, label the box score
        for box_score in scores.score_list:
            home_team = f"{year} {box_score.get_home_team()}"
            away_team = f"{year} {box_score.get_away_team()}"
            hof = offense_dataframe.query(f"team.str.startswith('{home_team}')")
            hdf = defense_dataframe.query(f"team.str.startswith('{home_team}')")
            aof = offense_dataframe.query(f"team.str.startswith('{away_team}')")
            adf = defense_dataframe.query(f"team.str.startswith('{away_team}')")
            if len(hof) == 0 or len(hdf) == 0 or \
                len(aof) == 0 or len(adf) == 0:
                continue
            home_offense_label = int(hof.iloc[0]["offense_overall"])
            home_defense_label = int(hdf.iloc[0]["defense_overall"])
            away_offense_label = int(aof.iloc[0]["offense_overall"])
            away_defense_label = int(adf.iloc[0]["defense_overall"])
            lbs = LabeledBoxScore(
                box_score.score_obj,
                home_offense=home_offense_label,
                home_defense=home_defense_label,
                away_offense=away_offense_label,
                away_defense=away_defense_label
            )
            labeled.append(lbs)
        
        # Write the labeled scores
        with open(f"./data/labeled/{year}.json", "w") as labeled_data:
            labeled_data.write(
                json.dumps(labeled, indent=4)
            )

def aggregate_boxscores(args: argparse.Namespace) -> None:
    """
    Execute the boxscore label subcommand

    Args:
    args (argparse.Namespace): The CLI args

    Returns:
    None
    """
    # Loop through each year
    years = [
        int(d.replace(".json", "")) for d in os.listdir("./data/raw")
    ]
    training = []
    testing = []
    validation = []
    for year in years:
        print(f"Aggregating year {year}")
        with open(f"./data/labeled/{year}.json") as labeled_data:
            labeled = json.load(labeled_data)
        for score in labeled:
            lbs = LabeledBoxScore(
                {
                    "date": score["date"],
                    "home_team": score["home_team"],
                    "home_score": score["home_score"],
                    "away_team": score["away_team"],
                    "away_score": score["away_score"]
                },
                score["home_offense"],
                score["home_defense"],
                score["away_offense"],
                score["away_defense"]
            )
            random_int = random.randint(0, 9)
            if random_int < 1:
                validation.append(lbs)
            elif random_int < 2:
                testing.append(lbs)
            else:
                training.append(lbs)
    with open("./data/processed/training.json", "w") as training_data:
        training_data.write(json.dumps(training, indent=4))
    with open("./data/processed/validation.json", "w") as validation_data:
        validation_data.write(json.dumps(validation, indent=4))
    with open("./data/processed/testing.json", "w") as testing_data:
        testing_data.write(json.dumps(testing, indent=4))
