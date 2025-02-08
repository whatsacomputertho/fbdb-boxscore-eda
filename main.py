import argparse
from cli.boxscore   import  list_boxscores, \
                            summarize_boxscores, \
                            visualize_boxscores, \
                            label_boxscores, \
                            aggregate_boxscores, \
                            boxscore_frequency, \
                            boxscore_tie_frequency, \
                            boxscore_tie_frequency_by_skill
from cli.cli        import  get_cli_args
from cli.labeled    import  get_skill_differential_score_summary, \
                            summarize_skill_differential_score_summary, \
                            visualize_skill_differential_score_summary, \
                            visualize_home_away_score_summary, \
                            train_mean_score_regression_model, \
                            train_std_score_regression_model

def main(args: argparse.Namespace) -> None:
    """
    Execute the football database box score EDA CLI

    Args:
    args (argparse.Namespace): The CLI args

    Returns:
    None
    """
    if args.command == "boxscore":
        if args.subcommand == "list":
            list_boxscores(args)
        elif args.subcommand == "summarize":
            summarize_boxscores(args)
        elif args.subcommand == "visualize":
            visualize_boxscores(args)
        elif args.subcommand == "label":
            label_boxscores(args)
        elif args.subcommand == "aggregate":
            aggregate_boxscores(args)
        elif args.subcommand == "frequency":
            boxscore_frequency(args)
        elif args.subcommand == "tie-frequency":
            boxscore_tie_frequency(args)
        elif args.subcommand == "tie-frequency-by-skill":
            boxscore_tie_frequency_by_skill(args)
        else:
            raise Exception(
                f"Unrecognized boxscore subcommand {args.subcommand}"
            )
    elif args.command == "labeled":
        if args.subcommand == "skill-diff-scores":
            get_skill_differential_score_summary()
        elif args.subcommand == "skill-diff-summary":
            summarize_skill_differential_score_summary(args)
        elif args.subcommand == "skill-diff-visualize":
            visualize_skill_differential_score_summary(args)
        elif args.subcommand == "home-away-visualize":
            visualize_home_away_score_summary()
        elif args.subcommand == "mean-score-train":
            train_mean_score_regression_model(args)
        elif args.subcommand == "std-score-train":
            train_std_score_regression_model(args)
        else:
            raise Exception(
                f"Unrecognized labeled subcommand {args.subcommand}"
            )
    else:
        raise Exception(
            f"Unrecognized command {args.command}"
        )

if __name__ == "__main__":
    main(get_cli_args())
