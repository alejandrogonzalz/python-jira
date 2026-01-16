import os
import yaml
from dotenv import load_dotenv

class ConfigManager:
    """
    Manages configuration for the Jira integration.
    It loads configuration from a YAML file and environment variables.
    """
    def __init__(self, config_path: str = "config.yaml"):
        # 1. Cargar variables de entorno (el Token)
        load_dotenv()
        
        # 2. Cargar configuración pública (YAML)
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"❌ No encuentro el archivo {config_path}")
            
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

    @property
    def jira_url(self) -> str:
        return self.config['jira']['url']

    @property
    def jira_email(self) -> str:
        return self.config['jira']['email']

    @property
    def jira_token(self) -> str:
        # Recuperamos el secreto del entorno, no del YAML
        token = os.getenv("JIRA_API_TOKEN")
        if not token:
            raise ValueError("❌ Falta la variable de entorno JIRA_API_TOKEN")
        return token

    def get_project_key(self, alias: str) -> str:
        """Obtiene la KEY real (ej. 'ECOMM') dado un alias (ej. 'tienda')"""
        projects = self.config.get('projects', {})
        if alias not in projects:
            raise ValueError(f"El proyecto '{alias}' no está definido en config.yaml")
        return projects[alias]['key']