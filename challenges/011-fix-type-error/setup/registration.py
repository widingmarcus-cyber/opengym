"""User registration module."""


def create_username(first_name, last_name, year_of_birth):
    """Build a username like 'john_doe_1990' from components.

    Args:
        first_name: str
        last_name: str
        year_of_birth: int

    Returns:
        str: lowercase username in format 'first_last_year'
    """
    username = first_name.lower() + "_" + last_name.lower() + "_" + year_of_birth
    return username


def build_profile(name, age, tags):
    """Build a user profile dictionary.

    Args:
        name: str - user's display name
        age: int - user's age
        tags: list of str - interest tags

    Returns:
        dict with keys: 'name', 'age', 'tags' (sorted copy of tags list)
    """
    profile = {
        "name": name,
        "age": age,
        "tags": sorted(tags),
    }
    return profile


def format_address(street, city, zip_code):
    """Format a mailing address string.

    Args:
        street: str
        city: str
        zip_code: int

    Returns:
        str: formatted as 'street, city zip_code'
    """
    return street + ", " + city + " " + zip_code


def calculate_age_in_months(age_years):
    """Convert age in years to age in months.

    Args:
        age_years: str (from form input, e.g. '25')

    Returns:
        int: age in months
    """
    return age_years * 12


def merge_preferences(defaults, overrides):
    """Merge two preference dicts, with overrides taking priority.

    Args:
        defaults: dict
        overrides: dict

    Returns:
        dict: merged preferences
    """
    merged = defaults.copy()
    for key in overrides:
        merged[key] = overrides[key]
    return list(merged)
