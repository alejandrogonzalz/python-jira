import pytest

from src.core.parser import MarkdownParser


# --- FIXTURE ---
@pytest.fixture
def parser():
    return MarkdownParser()


# --- TESTS ---


def test_parse_single_epic_simple(parser):
    """Prueba una Épica simple sin separador explícito (todo es descripción)."""
    markdown_content = """
# My First Epic
This is the description for the first epic.
It spans multiple lines.
"""
    epics = parser.parse(markdown_content)

    assert len(epics) == 1
    assert epics[0].title == "My First Epic"
    # Verificamos limpieza de espacios
    assert (
        epics[0].description
        == "This is the description for the first epic.\nIt spans multiple lines."
    )
    assert len(epics[0].stories) == 0


def test_parse_epic_with_separator_and_stories(parser):
    """
    Prueba CLAVE: Verifica que el parser respete el separador '# Historias'.
    Todo lo de arriba es descripción, todo lo de abajo son historias.
    """
    markdown_content = """
# Epic with Architecture Docs
This is technical documentation.
## Subtitulo Tecnico (No es historia)
- Detalle tecnico

# Historias

## Story 1
Description 1
- Criteria A
## Story 2
Description 2
"""
    epics = parser.parse(markdown_content)
    epic = epics[0]

    # 1. Verificar Título
    assert epic.title == "Epic with Architecture Docs"

    # 2. Verificar Descripción (Debe incluir el subtítulo técnico)
    assert "This is technical documentation." in epic.description
    assert "## Subtitulo Tecnico" in epic.description
    # Asegurar que NO se coló el separador en la descripción
    assert "# Historias" not in epic.description

    # 3. Verificar Historias (Solo deben ser 2)
    assert len(epic.stories) == 2
    assert epic.stories[0].title == "Story 1"
    assert epic.stories[0].acceptance_criteria == ["Criteria A"]
    assert epic.stories[1].title == "Story 2"


def test_parse_epic_implicit_stories(parser):
    """
    Prueba de retro-compatibilidad: Si el usuario NO pone '# Historias',
    pero usa '## Titulo', el parser nuevo (en modo legacy) podría no detectarlas
    si la lógica estricta requiere el separador.

    NOTA: Según tu lógica actual, si NO hay separador, TODO se considera descripción.
    Así que este test valida que NO se creen historias por error si falta el separador.
    """
    markdown_content = """
# Simple Epic
## Story attempt
This looks like a story but without the separator it is description.
"""
    epics = parser.parse(markdown_content)

    assert len(epics) == 1
    # Como no hay "# Historias", el '## Story attempt' se trata como documentación H2
    assert len(epics[0].stories) == 0
    assert "## Story attempt" in epics[0].description


def test_parse_story_content_separation(parser):
    """Verifica que se separen bien los criterios de la descripción dentro de una historia."""
    markdown_content = """
# Epic Title

# Historias

## Complex Story
Line 1 of description.
Line 2 of description.
- Criterion 1
- Criterion 2
Line 3 of description (should stay in description).
"""
    epics = parser.parse(markdown_content)
    story = epics[0].stories[0]

    assert story.title == "Complex Story"
    # El parser junta las líneas que no son bullets
    expected_desc = "Line 1 of description.\nLine 2 of description.\nLine 3 of description (should stay in description)."
    assert story.description == expected_desc
    assert story.acceptance_criteria == ["Criterion 1", "Criterion 2"]


def test_parse_no_h1_returns_empty(parser):
    """Si no hay un título #, retorna lista vacía."""
    markdown_content = """
Just text.
## Maybe a story?
No epic title defined.
"""
    epics = parser.parse(markdown_content)
    assert len(epics) == 0


@pytest.mark.parametrize(
    "separator",
    ["# Historias", "# HISTORIAS", "# Stories", "# User Stories", "# user stories"],
)
def test_parse_separator_variations(parser, separator):
    """Prueba que el regex del separador sea flexible con mayúsculas e inglés/español."""
    markdown_content = f"""
# Main Epic
Docs here.

{separator}

## Story A
Desc A
"""
    epics = parser.parse(markdown_content)
    assert len(epics[0].stories) == 1
    assert epics[0].stories[0].title == "Story A"
