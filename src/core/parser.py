import re
from dataclasses import dataclass, field
from typing import List, Optional

# --- 1. Modelos de Datos (Independientes de JIRA) ---
@dataclass
class UserStory:
    title: str
    description: str = ""
    acceptance_criteria: List[str] = field(default_factory=list)

    def add_line(self, line: str):
        # Detecta si es un criterio (lista con guion) o texto normal
        if line.strip().startswith("- "):
            self.acceptance_criteria.append(line.strip()[2:])
        else:
            self.description += line + "\n"

@dataclass
class Epic:
    title: str
    description: str = ""
    stories: List[UserStory] = field(default_factory=list)

    def add_line(self, line: str):
        self.description += line + "\n"

# --- 2. La Lógica del Parser ---
class MarkdownParser:
    def __init__(self):
        # Regex para detectar encabezados # y ##
        self.epic_pattern = re.compile(r'^#\s+(.+)$')
        self.story_pattern = re.compile(r'^##\s+(.+)$')

    def parse(self, content: str) -> List[Epic]:
        epics = []
        current_epic: Optional[Epic] = None
        current_story: Optional[UserStory] = None
        
        # Leemos línea por línea
        lines = content.splitlines()
        
        for line in lines:
            line = line.strip()
            if not line: continue  # Saltar líneas vacías

            # 1. Detectar Nueva Épica
            epic_match = self.epic_pattern.match(line)
            if epic_match:
                # Si había una historia abierta, ya se guardó en la épica anterior
                # Creamos nueva épica
                current_epic = Epic(title=epic_match.group(1))
                epics.append(current_epic)
                current_story = None # Reseteamos la historia
                continue

            # 2. Detectar Nueva Historia
            story_match = self.story_pattern.match(line)
            if story_match:
                if not current_epic:
                    raise ValueError(f"Error: Encontré una Historia '{line}' sin una Épica padre.")
                
                current_story = UserStory(title=story_match.group(1))
                current_epic.stories.append(current_story)
                continue

            # 3. Procesar Contenido (Descripción o Criterios)
            if current_story:
                # Si estamos dentro de una historia, el texto va para ella
                current_story.add_line(line)
            elif current_epic:
                # Si no hay historia, pero sí épica, es descripción de la épica
                current_epic.add_line(line)
        
        return epics