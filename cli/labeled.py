import argparse
import json
import matplotlib.pyplot
import pandas
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

def get_skill_differential_score_summary() -> None:
    """
    Compute the scoring summary for each skill differential
    """
    with open("./data/processed/training.json") as training_data:
        scores = json.load(training_data)
    summaries = []
    for score in scores:
        # Calculate the differentials for each team
        home_diff = score["home_offense"] - score["away_defense"]
        away_diff = score["away_offense"] - score["home_defense"]
        summaries.append({
            "offense_defense_differential": home_diff,
            "score": score["home_score"],
            "is_home": True
        })
        summaries.append({
            "offense_defense_differential": away_diff,
            "score": score["away_score"],
            "is_home": False
        })
    with open("./data/preprocessed/skill_diff_scores.json", "w") as skill_diff_data:
        skill_diff_data.write(json.dumps(summaries, indent=4))

def summarize_skill_differential_score_summary(
        args: argparse.Namespace
    ) -> None:
    """
    Summarize the scoring for each skill differential
    """
    with open("./data/preprocessed/testing_skill_diff_scores.json") as skill_diff_data:
        skill_diffs = json.load(skill_diff_data)
    diff_df = pandas.read_json(json.dumps(skill_diffs))
    diff_df["offense_defense_differential"] = (diff_df["offense_defense_differential"] + 4) / 8
    dest_filename = ""
    if args.home:
        diff_df = diff_df.query("is_home == True")
        dest_filename = "home"
    elif args.away:
        diff_df = diff_df.query("is_home == False")
        dest_filename = "away"
    summary = diff_df.groupby("offense_defense_differential").describe()
    summaries = []
    for i in range(len(summary)):
        summary_dict = {
            "norm_diff": summary.iloc[i].name,
            "mean_score": summary.iloc[i][1],
            "std_score": summary.iloc[i][2]
        }
        summaries.append(summary_dict)
    with open(f"./data/preprocessed/testing_{dest_filename}.json", "w") as out_data:
        out_data.write(json.dumps(summaries, indent=4))

def visualize_skill_differential_score_summary(
        args: argparse.Namespace
    ) -> None:
    """
    Visualize the scoring for each skill differential
    """
    with open("./data/preprocessed/skill_diff_scores.json") as skill_diff_data:
        skill_diffs = json.load(skill_diff_data)
    diff_df = pandas.read_json(json.dumps(skill_diffs))
    title = "Score summaries by offense-defense skill differential"
    if args.home:
        diff_df = diff_df.query("is_home == True")
        title += " (home offenses only)"
    elif args.away:
        diff_df = diff_df.query("is_home == False")
        title += " (away offenses only)"
    ax = diff_df.boxplot(column="score", by="offense_defense_differential")
    ax.set_title(title)
    ax.set_xlabel("Offense-defense skill differential")
    ax.set_ylabel("Scoring summaries")
    matplotlib.pyplot.show()

def visualize_home_away_score_summary() -> None:
    """
    Visualize the scoring for home teams versus away teams
    """
    with open("./data/preprocessed/skill_diff_scores.json") as skill_diff_data:
        skill_diffs = json.load(skill_diff_data)
    diff_df = pandas.read_json(json.dumps(skill_diffs))
    ax = diff_df.boxplot(column="score", by="is_home")
    ax.set_title("Score summaries for home versus away teams")
    ax.set_xlabel("Home/away")
    ax.set_ylabel("Scoring summaries")
    matplotlib.pyplot.show()

def train_mean_score_regression_model(args: argparse.Namespace) -> None:
    """
    Train a regression model for predicting mean score from the skill
    differential of the offense and defense
    """
    filename_prefix = "home"
    if args.away:
        filename_prefix = "away"
    summ_df = pandas.read_json(f"./data/preprocessed/{filename_prefix}.json")

    # Train a linear regression model for the mean scores
    mean_model = LinearRegression()
    mean_model.fit(summ_df[["norm_diff"]], summ_df[["mean_score"]])
    print(f"y = {mean_model.coef_}x + {mean_model.intercept_}")

    # Test the linear regression model using the test data
    test_df = pandas.read_json(f"./data/preprocessed/testing_{filename_prefix}.json")
    y_pred = mean_model.predict(test_df[["norm_diff"]])
    ax = matplotlib.pyplot.gca()
    ax.set_title(f"Mean {filename_prefix} score over normalized skill differential (linreg)")
    ax.set_xlabel("Normalized skill differential (offense versus defense)")
    ax.set_ylabel(f"Mean {filename_prefix} score")
    matplotlib.pyplot.scatter(summ_df[["norm_diff"]], summ_df[["mean_score"]], color='g')
    matplotlib.pyplot.plot(test_df[["norm_diff"]], y_pred, color='b')
    matplotlib.pyplot.show()

def train_std_score_regression_model(args: argparse.Namespace) -> None:
    """
    Train a regression model for predicting score std from the skill
    differential of the offense and defense
    """
    filename_prefix = "home"
    if args.away:
        filename_prefix = "away"
    summ_df = pandas.read_json(f"./data/preprocessed/{filename_prefix}.json")

    # Train a linear regression model for the score stdev
    pf = PolynomialFeatures(degree=2)
    t_norm_diff = pf.fit_transform(summ_df[["norm_diff"]])
    pf.fit(t_norm_diff, summ_df[["std_score"]])
    std_model = LinearRegression()
    std_model.fit(t_norm_diff, summ_df[["std_score"]])
    print(f"coef: {std_model.coef_}")
    print(f"intr: {std_model.intercept_}")

    # Test the linear regression model using the test data
    test_df = pandas.read_json(f"./data/preprocessed/testing_{filename_prefix}.json")
    y_pred = std_model.predict(pf.fit_transform(test_df[["norm_diff"]]))
    matplotlib.pyplot.scatter(summ_df[["norm_diff"]], summ_df[["std_score"]], color='g')
    matplotlib.pyplot.plot(summ_df[["norm_diff"]], y_pred, color='b')
    matplotlib.pyplot.title(f'Standard deviation of {filename_prefix} score over normalized skill differential (polyreg)')
    matplotlib.pyplot.xlabel('Normalized skill differential (offense versus defense)')
    matplotlib.pyplot.ylabel(f'Standard deviation of {filename_prefix} score')
    matplotlib.pyplot.show()
