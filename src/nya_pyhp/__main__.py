import sys
from pathlib import Path

import arguably

from . import interpolate


@arguably.command
def main(template_file: str, /, *, type: str = None):
	"""
	PyHP - PHP-like template engine for Python.

	Args:
	    template_file: Template file to process.
	    type: Template type (e.g., .html). If omitted, inferred from file extension.
	"""
	if type is None:
		type = Path(template_file).suffix or ".html"

	try:
		content = Path(template_file).read_text()

		# We might want to provide some default environment here for the CLI
		result = interpolate(content, type, filename=template_file)
		print(result, end="")
	except Exception:
		# Traceback is already printed in executor.py if it was a template error
		sys.exit(1)


def cli():
	arguably.run()


if __name__ == "__main__":
	cli()
