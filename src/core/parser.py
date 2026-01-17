import re
from dataclasses import dataclass, field
from typing import List, Optional


# --- Modelos ---
@dataclass
class UserStory:
    title: str
    description: str = ""
    acceptance_criteria: List[str] = field(default_factory=list)

    def set_content(self, raw_content: str):
        """Separa descripción de criterios"""
        lines = raw_content.strip().splitlines()
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue

            if stripped.startswith("- ") or stripped.startswith("* "):
                self.acceptance_criteria.append(stripped[2:])
            else:
                self.description += line + "\n"
        self.description = self.description.strip()


@dataclass
class Epic:
    title: str
    description: str = ""
    stories: List[UserStory] = field(default_factory=list)


# --- Parser con Soporte de Secciones ---
class MarkdownParser:
    """
    Parser avanzado que soporta documentación rica en la Épica.
    Busca un separador '# Historias' para saber cuándo terminan los docs y empiezan los tickets.
    """

    def parse(self, content: str) -> List[Epic]:
        # 1. Extraer el Título Principal (# Título)
        epic_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        if not epic_match:
            return []

        epic_title = epic_match.group(1).strip()
        full_content = content

        # 2. Buscar el SEPARADOR de Historias
        # Buscamos una línea que sea exactamente "# Historias" o "# Stories" (case insensitive)
        separator_regex = r"(?im)^#\s+(?:Historias|Stories|User Stories)\s*$"
        separator_match = re.search(separator_regex, full_content)

        epic_desc_text = ""
        stories_block = ""

        if separator_match:
            # CASO A: Hay separador.
            # La descripción es todo desde el inicio hasta antes del separador
            # (Quitamos la primera línea del título de la épica para no duplicarlo)
            split_index = separator_match.start()
            epic_desc_raw = full_content[:split_index]

            # Limpiamos el título principal de la descripción
            epic_desc_text = epic_desc_raw.replace(epic_match.group(0), "", 1).strip()

            # El bloque de historias es todo lo que sigue al separador
            stories_block = full_content[separator_match.end() :]

        else:
            # CASO B: No hay separador (Todo es descripción, 0 historias)
            # O el usuario olvidó poner "# Historias". Asumimos que todo es Épica.
            epic_desc_text = full_content.replace(epic_match.group(0), "", 1).strip()

        # Creamos la Épica
        epic = Epic(title=epic_title, description=epic_desc_text)

        # 3. Procesar las Historias (si existen) del bloque de historias
        if stories_block:
            # Aquí sí, cada "## " es una historia nueva
            sections = re.split(r"(?m)^##\s+(.+)$", stories_block)

            # sections[0] suele ser vacío o texto introductorio bajo "# Historias"
            for i in range(1, len(sections), 2):
                story_title = sections[i].strip()
                story_content = sections[i + 1] if i + 1 < len(sections) else ""

                story = UserStory(title=story_title)
                story.set_content(story_content)
                epic.stories.append(story)

        return [epic]
