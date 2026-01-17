from atlassian import Jira
from requests.exceptions import HTTPError
from typing import Optional

from .parser import Epic, UserStory
from .utils import JiraFormatter


class JiraAdapter:
    _instance = None
    _jira_client = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(JiraAdapter, cls).__new__(cls)
        return cls._instance

    def __init__(self, url: str, email: str, token: str, dry_run: bool = False):
        self.dry_run = dry_run

        # CAMBIO 1: Quitamos "and not self.dry_run"
        # Ahora nos conectamos SIEMPRE para poder validar el proyecto y buscar duplicados
        if not self._jira_client:
            try:
                self._jira_client = Jira(
                    url=url, username=email, password=token, cloud=True
                )
                # Validamos conexión haciendo una petición ligera (info del usuario)
                self._jira_client.myself()
                print(
                    f"✅ Conexión establecida con JIRA (Modo {'DRY-RUN' if dry_run else 'LIVE'})"
                )
            except Exception as e:
                raise ConnectionError(f"❌ Error conectando a JIRA: {e}")

    def get_existing_epic(self, project_key: str, title: str) -> Optional[str]:
        """Busca (REALMENTE) si ya existe una Épica."""
        # CAMBIO 2: Ya no hay "if dry_run return None". Buscamos de verdad.

        safe_title = title.replace('"', '\\"')
        jql = f'project = "{project_key}" AND issuetype = "Epic" AND summary ~ "\\"{safe_title}\\""'

        try:
            results = self._jira_client.jql(jql, limit=1)
            issues = results.get("issues", [])
            if issues:
                found_issue = issues[0]
                if found_issue["fields"]["summary"] == title:
                    return found_issue["key"]
            return None
        except Exception as e:
            print(f"   ⚠️ Error buscando duplicados (Epic): {e}")
            return None

    def get_existing_story(self, project_key: str, parent_key: str, title: str) -> bool:
        """Busca (REALMENTE) si ya existe una historia."""

        # Si la épica padre es falsa (MOCK), no buscamos en Jira porque fallará
        if parent_key.startswith("MOCK-"):
            return False

        safe_title = title.replace('"', '\\"')
        jql = f'project = "{project_key}" AND issuetype = "Story" AND parent = "{parent_key}" AND summary ~ "\\"{safe_title}\\""'

        try:
            results = self._jira_client.jql(jql)
            issues = results.get("issues", [])
            for issue in issues:
                if issue["fields"]["summary"] == title:
                    return True
            return False
        except Exception as e:
            return False

    def create_epic(self, project_key: str, epic: Epic) -> Optional[str]:
        """
        Lógica:
        1. Buscar si existe (REAL)
        2. Si no existe:
           - Si es DRY RUN -> Imprimir "Crearía" y devolver ID falso.
           - Si es LIVE -> Crear ticket real.
        """

        # 1. VERIFICACIÓN REAL (Incluso en Dry Run)
        existing_key = self.get_existing_epic(project_key, epic.title)
        if existing_key:
            print(
                f"   🔄 [EXISTE EN JIRA] La Épica ya existe: {existing_key} -> Reutilizando."
            )
            return existing_key

        # 2. Si no existe, preparamos creación
        fields = {
            "project": {"key": project_key},
            "summary": epic.title,
            "description": JiraFormatter.markdown_to_jira(epic.description),
            "issuetype": {"name": "Epic"},
        }

        # 3. INTERRUPTOR DRY RUN (Aquí es donde paramos la escritura)
        if self.dry_run:
            print(f"   🧪 [DRY-RUN] Se CREARÍA nueva Épica: '{epic.title}'")
            return "MOCK-EPIC-999"  # Retornamos ID falso para que el flujo continúe

        # 4. CREACIÓN REAL
        try:
            issue = self._jira_client.issue_create(fields=fields)
            print(f"✨ Épica creada: {issue['key']}")
            return issue["key"]
        except HTTPError as e:
            self._handle_error(e, epic.title)
            return None

    def create_story(self, project_key: str, parent_epic_key: str, story: UserStory):
        # 1. VERIFICACIÓN REAL
        if self.get_existing_story(project_key, parent_epic_key, story.title):
            print(f"   ⏭️  [EXISTE EN JIRA] La historia ya existe -> Saltando.")
            return

        desc_completa = JiraFormatter.markdown_to_jira(story.description)
        if story.acceptance_criteria:
            desc_completa += "\n\n*Criterios de Aceptación:*\n"
            for crit in story.acceptance_criteria:
                desc_completa += f"* {JiraFormatter.markdown_to_jira(crit)}\n"

        fields = {
            "project": {"key": project_key},
            "summary": story.title,
            "description": desc_completa,
            "issuetype": {"name": "Story"},
            "parent": {"key": parent_epic_key},
        }

        # 2. INTERRUPTOR DRY RUN
        if self.dry_run:
            print(
                f"   🧪 [DRY-RUN] Se CREARÍA Historia: '{story.title}' en {parent_epic_key}"
            )
            return

        # 3. CREACIÓN REAL
        try:
            self._jira_client.issue_create(fields=fields)
            print(f"   └─ ✅ Historia creada: {story.title}")
        except HTTPError as e:
            print(f"   ⚠️ Error creando historia '{story.title}': {e.response.text}")

    def _handle_error(self, error, context_title):
        try:
            error_response = error.response.json()
            error_list = error_response.get("errors", {})
            error_messages = error_response.get("errorMessages", [])
            print(f"\n⚠️  Error creando '{context_title}':")
            for field, msg in error_list.items():
                print(f"   ❌ Campo '{field}': {msg}")
            for msg in error_messages:
                print(f"   ❌ General: {msg}")
        except ValueError:
            print(f"⚠️ Error crítico: {error.response.text}")
