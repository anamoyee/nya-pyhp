import pyhp


def test_pyhp():
	template = """<ul>
\t<!-- {{! while row := fetch_row(): }} -->
\t\t<li><!--{{ row }}--></li>
</ul>"""

	rows = ["Alice", "Bob", "Charlie"]
	row_idx = 0

	def fetch_row():
		nonlocal row_idx
		if row_idx < len(rows):
			res = rows[row_idx]
			row_idx += 1
			return res
		return None

	env = {"fetch_row": fetch_row}

	try:
		result = pyhp.interpolate(template, ".html", env)
		print("Result:")
		print(result)
	except Exception:
		print("Caught exception as expected if there was an error")


if __name__ == "__main__":
	test_pyhp()
