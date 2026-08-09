import pytest

import nya_pyhp


def test_error_reporting():
	template = """
Line 1: OK
Line 2: <!-- {{ 1/0 }} -->
Line 3: OK
"""[1:-1]
	with pytest.raises(ZeroDivisionError):
		nya_pyhp.interpolate(template, ".html", filename="error_test.html")


if __name__ == "__main__":
	test_error_reporting()
