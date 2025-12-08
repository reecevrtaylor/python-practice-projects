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

    
def is_valid(user: dict[str, object]) -> bool:
    return user["age"] is not None and user["score"] is not None


def is_active(user: dict[str, object]) -> bool:
    return user["active"] is True


cleaned_users = [u for u in (clean_user(user) for user in raw_users) if u]
valid_users = [u for u in cleaned_users if is_valid(u)]
active_users = [u for u in cleaned_users if is_active(u)]
valid_active_users = [u for u in cleaned_users if is_valid(u) and is_active(u)]


def average(values: list[float]) -> float | None:
    if not values:
        return None
    return sum(values) / len(values)


report = {
    "total_users": len(cleaned_users),
    "valid_users": len(valid_users),
    "active_users": len(active_users),
    "average_age": average([u["age"] for u in valid_users]),
    "average_score": average([u["score"] for u in valid_users]),
    "max_score_active": max([u["score"] for u in active_users if u["score"] is not None], default=None),
    "min_score_active": min([u["score"] for u in active_users if u["score"] is not None], default=None)
}


print(report)