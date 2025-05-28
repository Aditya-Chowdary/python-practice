# utils.py
import dateparser
from datetime import datetime

def parse_datetime_string(datetime_str: str) -> datetime | None:
    """
    Parses a human-readable datetime string into a datetime object.
    Uses dateparser which is quite robust.
    Returns a timezone-naive datetime object.
    """
    if not datetime_str:
        return None
    try:
        # Settings to prefer future dates for ambiguous inputs like "Friday"
        # RETURN_AS_TIMEZONE_AWARE: False ensures we get naive datetime objects,
        # which are simpler to store in MySQL DATETIME type without timezone complications.
        parsed_date = dateparser.parse(datetime_str, settings={'PREFER_DATES_FROM': 'future', 'RETURN_AS_TIMEZONE_AWARE': False})
        if parsed_date:
            return parsed_date
        return None
    except Exception as e:
        print(f"Dateparser Error: Could not parse '{datetime_str}': {e}")
        return None

if __name__ == '__main__':
    print(parse_datetime_string("tomorrow at 5 PM"))
    print(parse_datetime_string("next Wednesday"))
    print(parse_datetime_string("in 2 hours"))
    print(parse_datetime_string("August 15th 10am"))
    print(parse_datetime_string("this evening"))