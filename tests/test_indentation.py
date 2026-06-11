import pyhp


def test_indentation_logic():
	# Test case: increasing indentation without while/if should add 'if True:'
	template = """
Items:
	Item 1
	Item 2
		Subitem A
"""[1:-1]
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
		Tab-indented
        Space-indented (treated as L=0)
	One tab
"""[1:-1]
	result_mixed = pyhp.interpolate(template_mixed, ".html")
	print("\nMixed indentation test result:")
	print(repr(result_mixed))


if __name__ == "__main__":
	test_indentation_logic()
