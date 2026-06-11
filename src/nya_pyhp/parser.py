import re

from .types import dataclass


@dataclass
class Token:
	line_no: int
	col_no: int


@dataclass
class TextToken(Token):
	text: str


@dataclass
class CodeToken(Token):
	code: str
	is_exec: bool

	def __post_init__(self):
		self.code = self.process_code(self.code)

	def process_code(self, code: str) -> str:
		return self.dedent_tabs(code)

	def dedent_tabs(self, code: str) -> str:
		lines = code.splitlines()
		if not lines:
			return ""
		common_tabs = None
		for line in lines:
			if not line.strip():
				continue
			tabs = 0
			for char in line:
				if char == "\t":
					tabs += 1
				else:
					break
			if common_tabs is None or tabs < common_tabs:
				common_tabs = tabs
		if common_tabs:
			lines = [line[common_tabs:] if line.startswith("\t" * common_tabs) else line for line in lines]
		return "\n".join(lines)

	def __repr__(self):
		return f"Code({'!' if self.is_exec else ''}{self.code!r}, L={self.line_no}, C={self.col_no})"


@dataclass
class TemplateLine:
	indent_level: int
	tokens: list[Token]
	line_no: int


def parse_template(text: str, prefix: str, suffix: str) -> list[TemplateLine]:
	pattern = re.compile(f"(?P<prefix>{prefix})(?P<type>!|)(?P<code>.*?)(?P<suffix>{suffix})", re.DOTALL)

	def get_pos(offset):
		line = text.count("\n", 0, offset) + 1
		last_newline = text.rfind("\n", 0, offset)
		col = offset - last_newline if last_newline != -1 else offset + 1
		return line, col

	all_matches = list(pattern.finditer(text))
	segments: list[Token] = []
	last_pos = 0
	for match in all_matches:
		if match.start() > last_pos:
			l, c = get_pos(last_pos)
			segments.append(TextToken(l, c, text[last_pos : match.start()]))

		code_start = match.start("code")
		l, c = get_pos(code_start)
		is_exec = match.group("type") == "!"
		segments.append(CodeToken(l, c, match.group("code"), is_exec))
		last_pos = match.end()

	if last_pos < len(text):
		l, c = get_pos(last_pos)
		segments.append(TextToken(l, c, text[last_pos:]))

	template_lines = []
	current_tokens = []
	current_line_indent = None
	current_line_no = None

	for seg in segments:
		if isinstance(seg, CodeToken):
			if current_line_no is None:
				current_line_no = seg.line_no
			current_tokens.append(seg)
		else:
			lines_in_text = seg.text.splitlines(keepends=True)
			if not lines_in_text:
				continue

			for i, line_content in enumerate(lines_in_text):
				actual_line_no = seg.line_no + i
				actual_col_no = seg.col_no if i == 0 else 1

				if current_line_indent is None:
					current_line_indent = 0
					for char in line_content:
						if char == "\t":
							current_line_indent += 1
						elif char == " ":
							continue
						else:
							break
					current_line_no = actual_line_no

				current_tokens.append(TextToken(actual_line_no, actual_col_no, line_content))

				if line_content.endswith(("\n", "\r")):
					template_lines.append(TemplateLine(current_line_indent, current_tokens, current_line_no))
					current_tokens = []
					current_line_indent = None
					current_line_no = None

	if current_tokens:
		if current_line_indent is None:
			current_line_indent = 0
		if current_line_no is None:
			current_line_no = 1
		template_lines.append(TemplateLine(current_line_indent, current_tokens, current_line_no))

	return template_lines
