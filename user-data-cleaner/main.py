from typing import Optional

# Summary

# Loads messy user data (represented as Python structures—not real files yet).
# Cleans and normalizes each user using parsing functions.
# Filters users based on activity and validity.
# Computes basic statistics from the cleaned data.
# Outputs a report summarizing the results.

# solidifies:
# type safety / checking
# list & dict comprehensions
# robust function design
# safe parsing
# control flow
# nested JSON traversal
# return types
# defensive coding
# building small, structured modules

raw_users = [
    {
        "username": "alice",
        "age": "30",
        "score": "7.5",
        "active": "yes",
    },
    {
        "username": "bob",
        "age": "abc",  # invalid
        "score": "3",
        "active": "no",
    },
    {
        "username": "cara",
        "score": "10.0",  # missing age
        "active": "true",
    },
    {
        "username": "dan",
        "age": "40",
        "score": "bad",  # invalid float
        "active": "true",
    },
    {
        "username": "eve",
        "age": "",         # empty string -> invalid int
        "score": "5.0",
        "active": "1",     # numeric truthy
    },
    {
        "username": "frank",
        "age": "29.5",     # float string -> invalid int
        "score": "9.1",
        "active": "yes",
    },
    {
        "username": "grace",
        "age": "-5",       # negative age (edge case but parseable)
        "score": "NaN",    # float('NaN') -> not None but special value
        "active": "true",
    },
    {
        "username": "heidi",
        "age": None,       # missing age
        "score": "7",
        "active": "maybe", # unrecognized boolean
    },
    {
        "username": "ivan",
        "age": "50",
        "score": "",       # empty score -> invalid float
        "active": "0",     # numeric falsy
    },
    {
        "username": "judy",
        "age": "27",
        "score": "8",
        "active": "1",  # different case
    },
    {
        "username": None,  # missing username -> cleaned out
        "age": "33",
        "score": "6.5",
        "active": "no",
    },
    {
        "username": "ken",
        "age": "abc",      # invalid age
        "score": "",       # invalid score
        "active": None,    # missing active
    },
    {
        "username": "lou",
        "age": "30",
        "score": 8.5,      # non-string score (float)
        "active": "yes",
    },
]


def parse_int_default(text: str | None, default: int | None) -> int | None:
    if text is None:
        return default
    try:
        return int(text)
    except (ValueError, TypeError):
        return default


def parse_float_default(text: str | float | None, default: float | None) -> float | None:
    if text is None:
        return default
    try:
        return float(text)
    except (ValueError, TypeError):
        return default


def parse_bool_safe(text: Optional[str]) -> Optional[bool]:
    if text is None:
        return None

    value = text.strip().lower()

    if value in ("yes", "true", "1"):
        return True
    if value in ("no", "false", "0"):
        return False

    return None


def clean_user(raw: dict[str, str]) -> dict[str, object]:
    username = raw.get("username")

    if username is None:
        return {}

    age: Optional[str] = raw.get("age")
    score: Optional[float] = raw.get("score")
    active: Optional[float] = raw.get("active")

    cleaned_age = parse_int_default(age, None)
    cleaned_score = parse_float_default(score, None)
    cleaned_active = parse_bool_safe(active)


    return {"username": username ,"age": cleaned_age, "score": cleaned_score, "active": cleaned_active}


cleaned_users = [u for u in (clean_user(user) for user in raw_users) if u]
valid_users = [user for user in cleaned_users if user.get("age") and user.get("score")]
active_users = [user for user in cleaned_users if user.get("active")]

def average_age(users: list[dict[str, object]]) -> float | None:
    ages = [float(user.get("age")) for user in users if user.get("age") is not None]
    if not ages:
        return None
    return round(sum(ages) / len(ages), 2)

def average_score(users: list[dict[str, object]]) -> Optional[float]:
    scores = [float(user.get("score")) for user in users if user.get("score") is not None]
    if not scores:
        return None
    return round(sum(scores) / len(scores), 2)

def max_active_score(users: list[dict[str, object]]) -> float | None:
    scores = [user.get("score") for user in users if user.get("score") is not None]

    # for learning purposes, do not use max()
    current_score = scores[0]

    for score in scores:
        if score > current_score:
            current_score = score
    
    return current_score

def min_active_score(users: list[dict[str, object]]) -> float | None:
    scores = [user.get("score") for user in users if user.get("score") is not None]

    # for learning purposes, do not use min()
    current_score = scores[0]

    for score in scores:
        if score < current_score:
            current_score = score
    
    return current_score

report = {
    "total_users": len(cleaned_users),
    "valid_users": len(valid_users),
    "active_users": len(active_users),
    "average_age": average_age(cleaned_users),
    "average_score": average_score(cleaned_users),
    "max_active_score": max_active_score(active_users),
    "min_active_score": min_active_score(active_users)
}

print(report)