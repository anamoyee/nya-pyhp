import pyhp


def test_indentation_logic():
	# Test case: increasing indentation without while/if should add 'if True:'
	template = """
Items:
\tItem 1
\tItem 2
\t\tSubitem A
"""
	# Expected behavior:
	# Line 1: L=0 -> Text("\nItems:\n")
	# Line 2: L=1 -> if True: \n __write("\tItem 1\n")
	# Line 3: L=1 -> __write("\tItem 2\n")
	# Line 4: L=2 -> if True: \n __write("\t\tSubitem A\n")

	result = pyhp.interpolate(template, ".html")
	print("Indentation test result:")
	print(repr(result))

	# Another test: Mixed spaces and tabs
	template_mixed = """
Start
\t\tTab-indented
        Space-indented (treated as L=0)
\tOne tab
"""
	result_mixed = pyhp.interpolate(template_mixed, ".html")
	print("\nMixed indentation test result:")
	print(repr(result_mixed))


if __name__ == "__main__":
	test_indentation_logic()
