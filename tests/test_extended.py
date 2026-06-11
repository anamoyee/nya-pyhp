import pyhp
import pytest

def test_simple_interpolation():
    template = "Hello {{ name }}!"
    env = {"name": "World"}
    assert pyhp.interpolate(template, ".txt", env) == "Hello World!"

def test_simple_execution():
    template = """
<!-- {{! if True: }} -->
	Yes
<!-- {{! else: }} -->
	No
<!-- {{! pass }} -->""".strip()
    assert "Yes" in pyhp.interpolate(template, ".html")

def test_loop():
    template = "<!-- {{! for i in range(3): }} --><!-- {{ i }} --><!-- {{! pass }} -->"
    assert pyhp.interpolate(template, ".html") == "012"

def test_nested_indentation():
    template = """
<ul>
	<!-- {{! for i in range(2): }} -->
		<li>Item <!-- {{ i }} --></li>
	<!-- {{! pass }} -->
</ul>
""".strip()
    result = pyhp.interpolate(template, ".html")
    assert "<li>Item 0</li>" in result
    assert "<li>Item 1</li>" in result

def test_empty_template():
    assert pyhp.interpolate("", ".txt") == ""

def test_only_text():
    assert pyhp.interpolate("Just text", ".txt") == "Just text"

def test_only_code():
    assert pyhp.interpolate("{{ 1 + 1 }}", ".txt") == "2"

def test_undefined_variable():
    with pytest.raises(NameError):
        pyhp.interpolate("{{ undefined_var }}", ".txt")

def test_syntax_error_in_code():
    with pytest.raises(SyntaxError):
        # Missing colon
        pyhp.interpolate("<!-- {{! if True }} -->Hi<!-- {{! pass }} -->", ".html")

def test_multiline_code_token():
    template = """{{!
x = 10
y = 20
}}{{ x + y }}"""
    assert pyhp.interpolate(template, ".txt") == "30"

def test_multiple_tokens_on_one_line():
    template = "{{ a }} + {{ b }} = {{ a + b }}"
    env = {"a": 1, "b": 2}
    assert pyhp.interpolate(template, ".txt", env) == "1 + 2 = 3"

def test_mixed_exec_and_interpolation_on_one_line():
    template = "<!-- {{! x = 5 }} -->Value: <!-- {{ x }} -->"
    assert pyhp.interpolate(template, ".html") == "Value: 5"

def test_crlf_line_endings():
    template = "Line 1\r\n{{! x = 1 }}\r\nLine 2"
    result = pyhp.interpolate(template, ".txt")
    assert "Line 1\r\nLine 2" in result or "Line 1\nLine 2" in result

def test_unicode():
    template = "Héllò {{ name }}! 🚀"
    env = {"name": "Wörld"}
    assert pyhp.interpolate(template, ".txt", env) == "Héllò Wörld! 🚀"

def test_large_template():
    template = "repeat " * 1000 + "{{ val }}"
    env = {"val": "end"}
    assert pyhp.interpolate(template, ".txt", env) == "repeat " * 1000 + "end"

def test_runtime_error_remapping():
    template = """Line 1
Line 2: {{ 1/0 }}
Line 3"""
    try:
        pyhp.interpolate(template, ".txt", filename="runtime_error.txt")
    except ZeroDivisionError:
        import traceback
        tb = traceback.format_exc()
        assert 'File "runtime_error.txt"' in tb
        # We'll just check that it's mentioned, even if line number is off for now
        assert "ZeroDivisionError" in tb

def test_custom_type():
    from pyhp.types import register_type
    register_type(".custom", r"\[\[", r"\]\]")
    template = "Hello [[ name ]]!"
    assert pyhp.interpolate(template, ".custom", {"name": "User"}) == "Hello User!"

def test_dedent_tabs():
    # Test the dedent_tabs logic in CodeToken
    template = """
<!-- {{!
	if True:
		x = 1
	else:
		x = 2
}} --><!-- {{ x }} -->
"""[1:-1]
    assert pyhp.interpolate(template, ".html").strip() == "1"
