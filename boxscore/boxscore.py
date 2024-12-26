import json
import pandas
from boxscore.boxscoreschema import BOX_SCORE_SCHEMA, BOX_SCORE_LIST_SCHEMA
from jsonschema import validate, ValidationError
from typing import Dict, Any, Type, Tuple, List

# Override the default JSON encoder
def wrapped_default(self, obj):
    return getattr(obj.__class__, "__json__", wrapped_default.default)(obj)
wrapped_default.default = json.JSONEncoder().default
json.JSONEncoder.original_default = json.JSONEncoder.default
json.JSONEncoder.default = wrapped_default

class BoxScore:
    @staticmethod
    def validate_static(score_obj: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validates box score JSON loaded into a dict

        Args:
        score_obj (dict): The box score JSON loaded into a dict

        Returns:
        bool: Whether the box score JSON was valid
        str: The error message if the box score JSON was invalid
        """
        try:
            validate(
                instance=score_obj,
                schema=BOX_SCORE_SCHEMA
            )
        except ValidationError as ve:
            return False, str(ve)
        return True, ""

    def __init__(self, score_obj: Dict[str, Any]) -> Type["BoxScore"]:
        """
        Constructor for the BoxScore class

        Args:
        score_obj (dict): The box score JSON loaded into a dict

        Returns:
        BoxScore: The loaded BoxScore object
        """
        valid, err = BoxScore.validate_static(score_obj)
        if not valid:
            raise ValidationError(err)
        self.score_obj = score_obj

    def get_date_str(self) -> str:
        """
        Returns the date of the game as a string

        Args:
        None

        Returns:
        str: The date the game occurred
        """
        return str(self.score_obj.get("date"))

    def get_away_team(self) -> str:
        """
        Returns the away team for this box score

        Args:
        None

        Returns:
        str: The away team name
        """
        return str(self.score_obj.get("away_team"))

    def get_away_score(self) -> int:
        """
        Returns the away team score for this box score

        Args:
        None

        Returns:
        int: The away team score
        """
        return int(self.score_obj.get("away_score"))

    def get_home_team(self) -> str:
        """
        Returns the home team for this box score

        Args:
        None

        Returns:
        str: The home team name
        """
        return str(self.score_obj.get("home_team"))

    def get_home_score(self) -> int:
        """
        Returns the home team score for this box score

        Args:
        None

        Returns:
        int: The home team score
        """
        return int(self.score_obj.get("home_score"))
    
    def __str__(self) -> str:
        """
        Serializes the BoxScore instance as a string

        Args:
        None

        Returns:
        str: The string-serialized BoxScore
        """
        return f"[{self.get_date_str()}] {self.get_home_team()} " + \
            f"{self.get_home_score()} - {self.get_away_team()} " + \
            f"{self.get_away_score()}"

    def __json__(self) -> Dict[str, Any]:
        """
        Serializes the BoxScore instance as a JSON dict

        Args:
        None

        Returns
        dict: The JSON-serialized BoxScore
        """
        return self.score_obj

class BoxScoreList:
    @staticmethod
    def validate_static(score_list: List[Dict[str, Any]]) -> Tuple[bool, str]:
        """
        Validates a list of box score dicts

        Args:
        score_list (list): The list of box score dicts

        Returns:
        bool: Whether the box score list was valid
        str: The error message if the box score list was invalid
        """
        try:
            validate(
                instance=score_list,
                schema=BOX_SCORE_LIST_SCHEMA
            )
        except ValidationError as ve:
            return False, str(ve)
        return True, ""

    def __init__(
            self, score_list: List[Dict[str, Any]]
        ) -> Type["BoxScoreList"]:
        """
        Constructor for the BoxScoreList class

        Args:
        score_list (list): The list of box score dicts

        Returns:
        BoxScoreList: The loaded BoxScoreList
        """
        valid, err = BoxScoreList.validate_static(score_list)
        if not valid:
            raise ValidationError(err)
        self.score_list = []
        for score in score_list:
            self.score_list.append(BoxScore(score))

    def to_box_score_season(self, year: int) -> Type["BoxScoreSeason"]:
        """
        Converts a BoxScoreList instance to a BoxScoreSeason

        Args:
        year (int): The year the season occurred

        Returns:
        BoxScoreSeason: The loaded BoxScoreSeason
        """
        season = BoxScoreSeason(year)
        for score in self.score_list:
            season.add_game(score)
        return season

    def get_team_scores(self, team: str) -> List[int]:
        """
        Returns a given team's scores from the list

        Args:
        team (str): The team name

        Returns:
        list: The team's scores from the list
        """
        scores = []
        for score in self.score_list:
            if team == score.get_home_team():
                scores.append({
                    "offense": score.get_home_score(),
                    "defense": score.get_away_score()
                })
            elif team == score.get_away_team():
                scores.append({
                    "offense": score.get_away_score(),
                    "defense": score.get_home_score()
                })
        return scores

    def summarize_team_scores(
            self, team: str
        ) -> Type["BoxScoreSummary"]:
        """
        For a given team, this function summarizes the boxplot metrics for
        all of the box scores in the box score list, and returns it as a
        pandas series

        Args:
        team (str): The team name

        Returns:
        pandas.Series: The boxplot metrics of the team's offensive scores
        pandas.Series: The boxplot metrics of the team's defensive scores
        """
        dataframe = pandas.read_json(json.dumps(self.get_team_scores(team)))
        offense = dataframe["offense"].describe()
        defense = dataframe["defense"].describe()
        return BoxScoreSummary(team, offense, defense)

    def __str__(self) -> str:
        """
        Serializes the BoxScoreList instance as a string

        Args:
        None

        Returns:
        str: The string-serialized BoxScoreList
        """
        return "\n".join(
            [ str(box_score) for box_score in self.score_list ]
        )

    def __json__(self) -> List[Dict[str, Any]]:
        """
        Serializes the BoxScoreList instance as a list of JSON dicts

        Args:
        None

        Returns
        list: The JSON-serialized BoxScoreList
        """
        return json.loads(json.dumps(self.score_list))

class BoxScoreSeason:
    def __init__(self, year: int) -> Type["BoxScoreSeason"]:
        """
        Constructor for the BoxScoreSeason class

        Args:
        year (int): The year the season occurred

        Returns:
        BoxScoreSeason: The initialized BoxScoreSeason
        """
        self.year = year
        self.season = {}

    def add_game(self, score: Type["BoxScore"]) -> None:
        """
        Adds a game to the season's worth of box scores

        Args:
        score (BoxScore): The score to add to the season

        Returns:
        None
        """
        home_team = score.get_home_team()
        away_team = score.get_away_team()
        if home_team not in self.season.keys():
            self.season[home_team] = []
        if away_team not in self.season.keys():
            self.season[away_team] = []
        score_dict = score.__json__()
        self.season[home_team].append(score_dict)
        self.season[away_team].append(score_dict)

    def get_teams(self) -> List[str]:
        """
        Returns the list of teams who participated in the season

        Args:
        None

        Returns:
        list: The list of team names who participated in the season
        """
        return [ str(key) for key in self.season.keys() ]

    def get_team_box_scores(self, team: str) -> Type["BoxScoreList"]:
        """
        For a given team, this returns that team's box scores for this season

        Args:
        team (str): The team name

        Returns:
        list: The list of the team's box scores
        """
        team_scores = self.season.get(team)
        if team_scores == None:
            raise KeyError(f"Team not found: {team}")
        return BoxScoreList(team_scores)

    def summarize(self) -> Dict[str, Any]:
        """
        Returns the box plot metrics as a dict of pandas Series for the season
        of box scores for each team, in terms of the team's offense and
        defense.

        Args:
        None

        Returns:
        dict: The mapping of team names to their summarized offense and defense
        """
        summary = BoxScoreSummaryList()
        for team in self.get_teams():
            team_box_scores = self.get_team_box_scores(team)
            team_summary = team_box_scores.summarize_team_scores(team)
            team_summary.team = f"{self.year} {team_summary.team}"
            summary.add_summary(team_summary)
        return summary

class BoxScoreSummary:
    def __init__(
            self, team: str, offense: pandas.Series, defense: pandas.Series
        ) -> Type["BoxScoreSummary"]:
        """
        Constructor for the BoxScoreSummary class

        Args:
        team (str): The team name
        offense (pandas.Series): The boxplot summary of the team's points for
            on offense
        defense (pandas.Series): The boxplot summary of the team's points
            against on defense
        
        Returns:
        BoxScoreSummary: The initialized BoxScoreSummary
        """
        self.team = team
        self.offense = offense
        self.defense = defense

    def __str__(self) -> str:
        """
        Serializes a BoxScoreSummary as a string

        Args:
        None

        Returns:
        str: The string-serialized BoxScoreSummary
        """
        return f"{self.team}\nOffense:" + \
            f"\n{self.offense.to_string()}\n\nDefense:" + \
            f"\n{self.defense.to_string()}"

    def __json__(self) -> Dict[str, Any]:
        """
        Serializes a BoxScoreSummary as a JSON dict

        Args:
        None

        Returns:
        dict: The JSON-serialized BoxScoreSummary
        """
        return {
            "team": self.team,
            "offense": json.loads(self.offense.to_json()),
            "defense": json.loads(self.defense.to_json())
        }

class BoxScoreSummaryList:
    def __init__(self) -> Type["BoxScoreSummaryList"]:
        """
        Constructor for the BoxScoreSummaryList class

        Args:
        None

        Returns:
        BoxScoreSummaryList: The initialized summary list
        """
        self.summary = []

    def add_summary(self, team: BoxScoreSummary) -> None:
        """
        Add a team to the summary list

        Args:
        team (BoxScoreSummary): The added team's summary

        Returns:
        None
        """
        self.summary.append(team)

    def add_summaries(self, teams: Type["BoxScoreSummaryList"]) -> None:
        """
        Extends the summary list with another summary list

        Args:
        teams (BoxScoreSummaryList): The list to extend onto this one

        Returns:
        None
        """
        self.summary.extend(teams.summary)

    def __json__(self) -> List[Dict[str, Any]]:
        """
        Serializes a summary list as a JSON list

        Args:
        None

        Returns:
        list: The JSON-serialized BoxScoreSummaryList
        """
        return [ team.__json__() for team in self.summary ]

    def __str__(self) -> str:
        """
        Serializes a summary list as a string

        Args:
        None

        Returns:
        str: The string-serialized BoxScoreSummaryList
        """
        return "\n\n".join([
            str(team) for team in self.summary
        ])
