

import re
from typing import Any, Union
from cleanjson.utils import INT_REGEX, FLOAT_REGEX, is_email, is_phone


def strip_whitespace(val: str) -> str:
    """Strip leading and trailing whitespace from string."""
    return val.strip() if isinstance(val, str) else val


def clean_email(val: str) -> str:
    """Normalize email address by trimming whitespace and lowercasing."""
    if not isinstance(val, str):
        return val
    return val.strip().lower()


def clean_phone(val: str) -> str:
    """Normalize phone number by keeping digits and optional leading '+'."""
    if not isinstance(val, str):
        return val
    val = val.strip()
    has_plus = val.startswith("+")
    digits = re.sub(r"\D", "", val)
    if not digits:
        return val
    return f"+{digits}" if has_plus else digits


def convert_type(val: Any) -> Any:
    """Attempt type conversion for string representations of numbers and booleans."""
    if not isinstance(val, str):
        return val

    s = val.strip()
    
    # Booleans
    if s.lower() == "true":
        return True
    if s.lower() == "false":
        return False
    if s.lower() == "null" or s.lower() == "none":
        return None

    # Integers
    if INT_REGEX.match(s):
        try:
            return int(s)
        except ValueError:
            pass

    # Floats
    if FLOAT_REGEX.match(s):
        try:
            return float(s)
        except ValueError:
            pass

    return val


def is_empty_value(val: Any, empty_values: set = None) -> bool:
    """Check if a value is considered empty (None, empty string, empty list/dict, etc.)."""
    if empty_values is not None:
        return val in empty_values

    if val is None:
        return True
    if isinstance(val, str) and not val.strip():
        return True
    if isinstance(val, (list, dict, set, tuple)) and len(val) == 0:
        return True
    return False
