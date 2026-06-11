from dataclasses import dataclass, field
from typing import Any


@dataclass
class TemplateType:
	name: str
	prefix: str  # Now treated as a regex pattern fragment
	suffix: str  # Now treated as a regex pattern fragment
	env: dict[str, Any] = field(default_factory=dict)


_TYPES: dict[str, TemplateType] = {}


def register_type(name: str, prefix: str, suffix: str, env: dict[str, Any] | None = None):
	_TYPES[name] = TemplateType(name, prefix, suffix, env or {})


def get_type(name: str) -> TemplateType:
	if name in _TYPES:
		return _TYPES[name]
	# Default fallback
	if name == ".html":
		# Using \s* to make spaces optional
		return TemplateType(".html", r"<!--\s*{{", r"}}\s*-->")
	return TemplateType(name, r"{{", r"}}")


# Register default .html type with optional spaces
register_type(".html", r"<!--\s*{{", r"}}\s*-->")
