import pytest

from src.core.parser import MarkdownParser


# --- FIXTURE ---
# En lugar de setUp(), usamos un fixture que entrega una instancia fresca
# del parser a cada test que lo solicite como argumento.
@pytest.fixture
def parser():
    return MarkdownParser()


# --- TESTS ---


def test_parse_single_epic_no_stories(parser):
    markdown_content = """
# My First Epic
This is the description for the first epic.
It spans multiple lines.
"""
    epics = parser.parse(markdown_content)

    assert len(epics) == 1
    assert epics[0].title == "My First Epic"
    # Verificamos que respete los saltos de línea en la descripción
    assert (
        epics[0].description.strip()
        == "This is the description for the first epic.\nIt spans multiple lines."
    )
    assert len(epics[0].stories) == 0


def test_parse_epic_with_single_story_no_description(parser):
    markdown_content = """
# Another Epic
## A Simple Story
"""
    epics = parser.parse(markdown_content)

    assert len(epics) == 1
    assert epics[0].title == "Another Epic"
    assert epics[0].description.strip() == ""

    # Verificaciones de la historia hija
    assert len(epics[0].stories) == 1
    story = epics[0].stories[0]
    assert story.title == "A Simple Story"
    assert story.description.strip() == ""
    assert len(story.acceptance_criteria) == 0


def test_parse_epic_with_single_story_with_description_and_ac(parser):
    markdown_content = """
# Epic with AC
This is an epic with acceptance criteria.
## Story with AC
This is a story description.
- Criterion 1
- Criterion 2
Some more description.
"""
    epics = parser.parse(markdown_content)

    assert len(epics) == 1
    epic = epics[0]
    story = epic.stories[0]

    assert epic.title == "Epic with AC"
    assert epic.description.strip() == "This is an epic with acceptance criteria."

    assert story.title == "Story with AC"
    # Verificamos que el parser separó la lista (Criterios) del texto plano (Descripción)
    assert (
        story.description.strip()
        == "This is a story description.\nSome more description."
    )
    assert story.acceptance_criteria == ["Criterion 1", "Criterion 2"]


def test_parse_multiple_epics_and_stories(parser):
    markdown_content = """
# Epic Alpha
Description for Alpha.
## Story A1
Story A1 description.
- AC A1.1
## Story A2
Story A2 description.

# Epic Beta
Description for Beta.
## Story B1
Story B1 description.
- AC B1.1
- AC B1.2
"""
    epics = parser.parse(markdown_content)
    assert len(epics) == 2

    # Verificando Epic Alpha
    alpha = epics[0]
    assert alpha.title == "Epic Alpha"
    assert len(alpha.stories) == 2
    assert alpha.stories[0].title == "Story A1"
    assert alpha.stories[0].acceptance_criteria == ["AC A1.1"]
    assert alpha.stories[1].title == "Story A2"

    # Verificando Epic Beta
    beta = epics[1]
    assert beta.title == "Epic Beta"
    assert len(beta.stories) == 1
    assert beta.stories[0].title == "Story B1"
    assert beta.stories[0].acceptance_criteria == ["AC B1.1", "AC B1.2"]


def test_parse_no_epics(parser):
    markdown_content = """
This is just some plain text.
No epics or stories here.
"""
    epics = parser.parse(markdown_content)
    assert len(epics) == 0


def test_parse_story_without_epic_raises_error(parser):
    markdown_content = """
## Orphan Story
This story has no parent epic.
"""
    # pytest.raises con match reemplaza a assertRaisesRegex
    # El match busca texto parcial dentro del mensaje de error
    with pytest.raises(
        ValueError, match="Encontré una Historia .* sin una Épica padre"
    ):
        parser.parse(markdown_content)


# Agrupamos casos vacíos o solo espacios en un solo test parametrizado
@pytest.mark.parametrize(
    "content",
    [
        "",  # Vacío total
        "   \n \t \n",  # Solo espacios en blanco
    ],
)
def test_parse_empty_or_whitespace(parser, content):
    epics = parser.parse(content)
    assert len(epics) == 0
