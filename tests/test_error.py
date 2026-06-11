import pyhp
import pytest


def test_error_reporting():
	template = """
Line 1: OK
Line 2: <!-- {{ 1/0 }} -->
Line 3: OK
"""
	with pytest.raises(ZeroDivisionError):
		pyhp.interpolate(template, ".html", filename="error_test.html")


if __name__ == "__main__":
	test_error_reporting()
