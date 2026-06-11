from typing import Any

from .executor import execute_template
from .generator import generate_python
from .parser import parse_template
from .types import get_type


def interpolate(text: str, type_name: str, env: dict[str, Any] | None = None, filename: str = "<template>") -> str:
	t_type = get_type(type_name)

	# Merge environments
	full_env = t_type.env.copy()
	if env:
		full_env.update(env)

	# 1. Parse
	template_lines = parse_template(text, t_type.prefix, t_type.suffix)

	# 2. Generate
	python_code, mapping = generate_python(template_lines)

	# 3. Execute
	return execute_template(python_code, full_env, filename, mapping, text)
