BOX_SCORE_SCHEMA = {
    "type": "object",
    "description": "A box score from a football game",
    "additionalProperties": False,
    "properties": {
        "date": {
            "type": "string",
            "description": "The date the game occurred"
        },
        "away_team": {
            "type": "string",
            "description": "The away team name"
        },
        "away_score": {
            "type": "integer",
            "description": "The away team score"
        },
        "home_team": {
            "type": "string",
            "description": "The home team name"
        },
        "home_score": {
            "type": "integer",
            "description": "The home team score"
        },
    }
}

BOX_SCORE_LIST_SCHEMA = {
    "type": "array",
    "description": "A list of fooball box scores",
    "items": BOX_SCORE_SCHEMA
}
