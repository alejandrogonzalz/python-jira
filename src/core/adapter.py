import os
from atlassian import Jira
from requests.exceptions import HTTPError
from typing import Optional

from parser import Epic, UserStory 

class JiraAdapter:
    _instance = None
    _jira_client = None
    
    def __new__(cls, *args, **kwargs):
        """Implementación del patrón Singleton"""
        if cls._instance is None:
            cls._instance = super(JiraAdapter, cls).__new__(cls)
        return cls._instance

    def __init__(self, url: str, email: str, token: str, dry_run: bool = False):
        """
        Inicializa la conexión solo si no existe ya.
        dry_run: Si es True, simula la creación sin llamar a la API.
        """
        self.dry_run = dry_run
        
        # Evitamos re-inicializar si ya tenemos cliente (idempotencia del singleton)
        if not self._jira_client and not self.dry_run:
            try:
                self._jira_client = Jira(
                    url=url,
                    username=email,
                    password=token,
                    cloud=True
                )
                print(f"Conectado a JIRA: {url}")
            except Exception as e:
                raise ConnectionError(f"❌ Error conectando a JIRA: {e}")

    def create_epic(self, project_key: str, epic: Epic) -> Optional[str]:
        """Crea la Épica y retorna su KEY (ej: PROJ-10)"""
        
        fields = {
            "project": {"key": project_key},
            "summary": epic.title,
            "description": epic.description,
            "issuetype": {"name": "Epic"},
            # Campo obligatorio para Epics en muchos Jiras
            "customfield_10011": epic.title  # "Epic Name" (el ID del campo varía según la instancia)
        }

        if self.dry_run:
            print(f"[DRY-RUN] Crearía ÉPICA: {epic.title}")
            return "MOCK-EPIC-001"

        try:
            issue = self._jira_client.issue_create(fields=fields)
            print(f"✨ Épica creada: {issue['key']}")
            return issue['key']
        except HTTPError as e:
            print(f"⚠️ Error creando épica '{epic.title}': {e.response.text}")
            return None

    def create_story(self, project_key: str, parent_epic_key: str, story: UserStory):
        """Crea una Historia y la vincula a la Épica padre"""
        
        # Convertimos la lista de criterios en texto formateado para JIRA
        desc_completa = story.description
        if story.acceptance_criteria:
            desc_completa += "\n\n*Criterios de Aceptación:*\n"
            for crit in story.acceptance_criteria:
                desc_completa += f"* {crit}\n"

        fields = {
            "project": {"key": project_key},
            "summary": story.title,
            "description": desc_completa,
            "issuetype": {"name": "Story"},
            # Vinculación Padre-Hijo (en Jira Cloud moderno se usa 'parent')
            "parent": {"key": parent_epic_key}
        }

        if self.dry_run:
            print(f"   [DRY-RUN] Crearía STORY vinculada a {parent_epic_key}: {story.title}")
            return

        try:
            self._jira_client.issue_create(fields=fields)
            print(f"   └─ Historia creada: {story.title}")
        except HTTPError as e:
            print(f"   ⚠️ Error creando historia '{story.title}': {e.response.text}")