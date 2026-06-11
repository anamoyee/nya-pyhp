import io
import linecache
import re
import sys
import traceback
from typing import Any


def execute_template(python_code: str, env: dict[str, Any], filename: str, mapping: dict[int, tuple[int, int]], template_source: str):
	linecache.cache[filename] = (len(python_code), None, python_code.splitlines(keepends=True), filename)

	output = []

	def write(s):
		output.append(str(s))

	exec_globals = {}

	try:
		try:
			code_obj = compile(python_code, filename, "exec")
		except SyntaxError as e:
			# SyntaxError (including IndentationError) during compile
			# Map it back to the template
			t_line, t_col = mapping.get(e.lineno, (e.lineno or 1, e.offset or 1))
			template_lines = template_source.splitlines()
			t_text = template_lines[t_line - 1] if 1 <= t_line <= len(template_lines) else ""

			# Clean up the message (remove "on line X" which refers to generated code)
			msg = re.sub(r" on line \d+", "", e.msg)

			# Create a re-mapped SyntaxError/IndentationError
			new_exc = type(e)(msg, (filename, t_line, t_col, t_text))
			
			# Raise the new exception without the internal traceback
			raise new_exc from None

		exec(code_obj, exec_globals)

		if "__render" in exec_globals:
			exec_globals["__render"](env, write)

	except Exception:
		exc_type, exc_value, tb = sys.exc_info()

		# If it's a SyntaxError that we already handled
		if isinstance(exc_value, SyntaxError) and not tb:
			raise

		# For runtime errors, we could also re-map them here if we wanted to suppress 
		# the internal traceback entirely, but for now we'll just stop manual printing.
		raise

	return "".join(output)
