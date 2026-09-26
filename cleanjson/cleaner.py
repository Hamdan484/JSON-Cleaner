

from typing import Any, Dict, List, Optional, Callable, Set, Union
from cleanjson.rules import (
    strip_whitespace,
    clean_email,
    clean_phone,
    convert_type,
    is_empty_value,
)
from cleanjson.utils import is_email, is_phone


class Cleaner:
    """Configurable data cleaning engine."""

    def __init__(
        self,
        strip_whitespace: bool = True,
        normalize_emails: bool = True,
        normalize_phones: bool = True,
        convert_types: bool = True,
        drop_empty: bool = False,
        dedupe_lists: bool = True,
        custom_rules: Optional[Dict[str, Callable[[Any], Any]]] = None,
    ):
        self.strip_whitespace = strip_whitespace
        self.normalize_emails = normalize_emails
        self.normalize_phones = normalize_phones
        self.convert_types = convert_types
        self.drop_empty = drop_empty
        self.dedupe_lists = dedupe_lists
        self.custom_rules = custom_rules or {}

    def clean(self, data: Any) -> Any:
        """Entry point to clean arbitrary data structures."""
        return self._clean_node(data, key_name="")

    def _clean_node(self, val: Any, key_name: str = "") -> Any:
        # Check custom rules first if key matches
        if key_name and key_name in self.custom_rules:
            val = self.custom_rules[key_name](val)

        if isinstance(val, dict):
            return self._clean_dict(val)

        if isinstance(val, list):
            return self._clean_list(val, key_name)

        if isinstance(val, tuple):
            return tuple(self._clean_list(list(val), key_name))

        if isinstance(val, set):
            cleaned = self._clean_list(list(val), key_name)
            return set(cleaned)

        if isinstance(val, str):
            return self._clean_string(val, key_name)

        return val

    def _clean_dict(self, d: Dict[Any, Any]) -> Dict[Any, Any]:
        cleaned_dict = {}
        for k, v in d.items():
            clean_k = strip_whitespace(k) if isinstance(k, str) and self.strip_whitespace else k
            clean_v = self._clean_node(v, key_name=str(clean_k))

            if self.drop_empty and is_empty_value(clean_v):
                continue

            cleaned_dict[clean_k] = clean_v
        return cleaned_dict

    def _clean_list(self, lst: List[Any], key_name: str = "") -> List[Any]:
        cleaned_list = []
        for item in lst:
            cleaned_item = self._clean_node(item, key_name=key_name)

            if self.drop_empty and is_empty_value(cleaned_item):
                continue

            cleaned_list.append(cleaned_item)

        if self.dedupe_lists:
            cleaned_list = self._dedupe_list(cleaned_list)

        return cleaned_list

    def _clean_string(self, val: str, key_name: str = "") -> Any:
        if self.strip_whitespace:
            val = strip_whitespace(val)

        # Check if email
        if self.normalize_emails and is_email(val, key_name=key_name):
            return clean_email(val)

        # Check if phone
        if self.normalize_phones and is_phone(val, key_name=key_name):
            return clean_phone(val)

        # Convert type (integers, floats, booleans)
        if self.convert_types:
            return convert_type(val)

        return val

    @staticmethod
    def _dedupe_list(lst: List[Any]) -> List[Any]:
        """Deduplicate list items preserving order, supporting unhashable types."""
        unique = []
        for item in lst:
            if item not in unique:
                unique.append(item)
        return unique


def clean(
    data: Any,
    strip_whitespace: bool = True,
    normalize_emails: bool = True,
    normalize_phones: bool = True,
    convert_types: bool = True,
    drop_empty: bool = False,
    dedupe_lists: bool = True,
    custom_rules: Optional[Dict[str, Callable[[Any], Any]]] = None,
) -> Any:
    """Convenience function to clean data with default or custom options."""
    cleaner = Cleaner(
        strip_whitespace=strip_whitespace,
        normalize_emails=normalize_emails,
        normalize_phones=normalize_phones,
        convert_types=convert_types,
        drop_empty=drop_empty,
        dedupe_lists=dedupe_lists,
        custom_rules=custom_rules,
    )
    return cleaner.clean(data)
