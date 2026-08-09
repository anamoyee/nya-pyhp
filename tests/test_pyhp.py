import nya_pyhp


def test_pyhp():
	template = """
<ul>
	<!-- {{! while row := fetch_row(): }} -->
		<li><!--{{ row }}--></li>
</ul>
"""[1:-1]

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

	result = nya_pyhp.interpolate(template, ".html", env)

	assert (
		result
		== """
<ul>
		<li>Alice</li>
		<li>Bob</li>
		<li>Charlie</li>
</ul>
"""[1:-1]
	)
