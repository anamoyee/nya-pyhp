from .parser import CodeToken, TemplateLine, TextToken, Token


def generate_python(template_lines: list[TemplateLine]) -> tuple[str, dict[int, tuple[int, int]]]:
	python_lines = []
	line_mapping = {}

	indent_stack = [0]

	def add_line(line, template_token: Token | None = None):
		python_level = len(indent_stack)
		python_lines.append("\t" * python_level + line)
		if template_token:
			line_mapping[len(python_lines)] = (template_token.line_no, template_token.col_no)

	python_lines.append("def __render(__env, __write):")
	line_mapping[1] = (1, 1)

	python_lines.append("\t" + "for __k, __v in __env.items(): globals()[__k] = __v")
	line_mapping[2] = (1, 1)

	last_was_block_starter = False

	for line in template_lines:
		# 1. Handle indentation change
		while len(indent_stack) > 1 and line.indent_level <= indent_stack[-1]:
			indent_stack.pop()

		if line.indent_level > indent_stack[-1]:
			if not last_was_block_starter:
				add_line("if True:")
				indent_stack.append(line.indent_level)
			else:
				# We already have a block starter, just record this level
				indent_stack.append(line.indent_level)

		last_was_block_starter = False

		# 2. Check for pure exec line
		has_exec = any(isinstance(t, CodeToken) and t.is_exec for t in line.tokens)
		has_non_exec = any(isinstance(t, CodeToken) and not t.is_exec for t in line.tokens)
		all_text_is_whitespace = all(not t.text.strip() for t in line.tokens if isinstance(t, TextToken))
		is_pure_exec = has_exec and not has_non_exec and all_text_is_whitespace

		# 3. Process tokens
		for token in line.tokens:
			if isinstance(token, TextToken):
				if token.text and not is_pure_exec:
					add_line(f"__write({token.text!r})", token)
			elif isinstance(token, CodeToken):
				if token.is_exec:
					code = token.code.strip()
					if code.endswith(":"):
						add_line(code, token)
						indent_stack.append(line.indent_level)
						last_was_block_starter = True
					else:
						for subline in code.splitlines():
							add_line(subline, token)
				else:
					add_line(f"__write({token.code.strip()})", token)

	return "\n".join(python_lines), line_mapping
