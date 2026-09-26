"""
Utility regex patterns and detection functions for cleanjson.
"""

import re

EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
)

# Matches phone number formats like +1 (555) 123-4567, 555-123-4567, etc.
PHONE_REGEX = re.compile(
    r"^\+?[\d\s\-\(\)\.]{7,25}$"
)

INT_REGEX = re.compile(r"^-?\d+$")
FLOAT_REGEX = re.compile(r"^-?\d+\.\d+$")

PHONE_KEYS = {"phone", "mobile", "tel", "fax", "telephone", "cell", "phone_number", "mobile_number"}
EMAIL_KEYS = {"email", "email_address", "mail"}


def is_email(val: str, key_name: str = "") -> bool:
    """Check if a string or key implies an email address."""
    clean_val = val.strip()
    if EMAIL_REGEX.match(clean_val):
        return True
    if key_name and key_name.strip().lower() in EMAIL_KEYS:
        return "@" in clean_val
    return False


def is_phone(val: str, key_name: str = "") -> bool:
    """Check if a string or key implies a phone number."""
    clean_val = val.strip()
    if key_name and key_name.strip().lower() in PHONE_KEYS:
        # Check if contains at least 5 digits
        digits = re.sub(r"\D", "", clean_val)
        return len(digits) >= 5
    # Strict regex check for values without specific key context
    if PHONE_REGEX.match(clean_val):
        digits = re.sub(r"\D", "", clean_val)
        # Avoid matching simple short numbers like '123'
        return 7 <= len(digits) <= 15
    return False
