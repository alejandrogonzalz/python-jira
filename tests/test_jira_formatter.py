import pytest
from src.core.utils import JiraFormatter

# 1. Agrupamos pruebas similares usando parametrize
# Esto ejecuta la función 4 veces con distintos inputs
@pytest.mark.parametrize("markdown, expected", [
    ("# Epic Title", "h2. Epic Title"),
    ("## Story Title", "h3. Story Title"),
    ("### Sub-Story", "h4. Sub-Story"),
    ("#### Sub-Sub-Story", "#### Sub-Sub-Story"), # Límite de conversión actual
])
def test_headers(markdown, expected):
    assert JiraFormatter.markdown_to_jira(markdown) == expected

@pytest.mark.parametrize("markdown, expected", [
    ("**bold text**", "*bold text*"),
    ("some **bold** text", "some *bold* text"),
    ("`inline code`", "{{inline code}}"),
    ("text with `code` snippet", "text with {{code}} snippet"),
])
def test_inline_styles(markdown, expected):
    assert JiraFormatter.markdown_to_jira(markdown) == expected

@pytest.mark.parametrize("markdown, expected", [
    ("[Google](https://www.google.com)", "[Google|https://www.google.com]"),
    ("Visit [Docs](https://docs.example.com)", "Visit [Docs|https://docs.example.com]"),
])
def test_links(markdown, expected):
    assert JiraFormatter.markdown_to_jira(markdown) == expected

@pytest.mark.parametrize("markdown, expected", [
    ("- Item 1", "* Item 1"),
    ("  - Item 2", "  * Item 2"),
    ("* Item 3", "* Item 3"), # Si ya es asterisco, se mantiene
])
def test_lists(markdown, expected):
    assert JiraFormatter.markdown_to_jira(markdown) == expected

# 2. Pruebas de bloques (multilínea)
def test_multiline_code_block():
    markdown = "```python\nprint('Hello')\n```"
    expected = "{code:python}\nprint('Hello')\n{code}"
    assert JiraFormatter.markdown_to_jira(markdown) == expected

def test_generic_code_block():
    markdown = "```\nplain text\n```"
    expected = "{code}\nplain text\n{code}"
    assert JiraFormatter.markdown_to_jira(markdown) == expected

# 3. Prueba de Integración (Todo junto)
def test_combined_markdown():
    markdown_text = """
# My Epic
## My Story
This is a **description** with a [link](https://example.com).
- Item one
- Item two
```python
print("hello world")
"""