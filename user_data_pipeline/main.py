"""
USER ANALYTICS MINI-PIPELINE
--------------------------------------------------------

INPUT EXAMPLE:
users = [
    {"id": 101, "name": "Alice", "age": 30, "cities": ["London", "Madrid"]},
    {"id": 102, "name": "Bob", "age": 20, "cities": ["Paris"]},
    {"id": 103, "name": "Charlie", "cities": ["London", "Berlin", "Paris"]},
    {"id": 104, "name": "Alice", "age": 30, "cities": ["London"]},
]

--------------------------------------------------------
TASK 1 — Extract All Unique Cities (SET)
• Use a set comprehension
• Remove duplicates across all users
• Optionally sort the result

--------------------------------------------------------
TASK 2 — Build Mapping: name → list of cities (DICT)
• Create a dictionary where each key is a user's name
• Value: list of all cities they appear with in the dataset
• Use dict.get() to accumulate city lists safely

--------------------------------------------------------
TASK 3 — Build List of Tuples: (name, number_of_cities)
• Use a list comprehension
• Count how many cities each user has visited
• Output example: [("Alice", 3), ("Bob", 1), ("Charlie", 3)]

--------------------------------------------------------
TASK 4 — Find Users With ≥ 2 Cities (LIST COMPREHENSION)
• Filter by len(cities) >= 2
• Result: list of user names

--------------------------------------------------------
TASK 5 — Identify Missing Required Fields (DICT + SET OPS)
• Required fields: {"id", "name", "age", "cities"}
• For each user, compute which keys are missing
• Use a set difference: required - set(user.keys())
• Output example: {103: {"age"}}

--------------------------------------------------------
TASK 7 — Package Final Results (DICT)
• Produce a dictionary such as:
    {
        "cities_all_unique": ...,
        "name_to_cities": ...,
        "city_counts": ...,
        "multi_city_users": ...,
        "missing_fields": ...,
    }
--------------------------------------------------------
"""

users = [
    {"id": 101, "name": "Alice", "age": 30, "cities": ["London", "Madrid"]},
    {"id": 102, "name": "Bob", "age": 20, "cities": ["Paris"]},
    {"id": 103, "name": "Charlie", "cities": ["London", "Berlin", "Paris"]},
    {"id": 104, "name": "Alice", "age": 30, "cities": ["London"]},
]


def unique_cities(user_list):
    return {city for user in user_list for city in user.get("cities", [])}


def map_name_to_cities(user_list):
    name_to_cities = {}
    for user in user_list:
        name = user.get("name")
        if name:
            cities = user.get("cities", [])
            name_to_cities[name] = name_to_cities.get(name, []) + cities
    return name_to_cities


def city_counts(user_list):
    return [
        (user.get("name"), len(user.get("cities", [])))
        for user in user_list
        if user.get("name")
    ]


def multiple_cities(user_list):
    return [user.get("name") for user in user_list if len(user.get("cities", [])) >= 2]


def missing_fields(user_list):
    required_fields = {"id", "name", "age", "cities"}
    result = {}
    for user in user_list:
        missing = required_fields - set(user.keys())
        if missing:
            result[user.get("id")] = missing
    return result


def build_package_results():
    return {
        "Unique Cities": unique_cities(users),
        "Names to Cities": map_name_to_cities(users),
        "City Counts": city_counts(users),
        "Multiple City Users": multiple_cities(users),
        "Missing Fields": missing_fields(users),
    }


if __name__ == "__main__":
    result = build_package_results()
    for key, value in result.items():
        print(f"{key}: {value}")
