import pytest
from unittest.mock import patch, mock_open
from src.config.config_manager import ConfigManager

# 1. Definimos los datos de prueba como una variable o fixture
VALID_YAML = """
jira:
  url: "https://test.atlassian.net"
  email: "test@example.com"
projects:
  test_alias:
    key: "TESTKEY"
"""


# 2. Test simple (sin Clases)
@patch('src.config.config_manager.load_dotenv')
@patch('os.path.exists', return_value=True)
@patch('builtins.open', new_callable=mock_open, read_data=VALID_YAML)
@patch('os.getenv', return_value="mock_token_123")
def test_init_success(mock_load_dotenv, mock_getenv, mock_file, mock_exists):
    # Ejecución
    cfg = ConfigManager(config_path="mock_config.yaml")

    # Aserciones limpias (Pytest Magic)
    assert cfg.jira_url == "https://test.atlassian.net"
    assert cfg.jira_email == "test@example.com"
    assert cfg.jira_token == "mock_token_123"
    assert cfg.get_project_key("test_alias") == "TESTKEY"


@patch('src.config.config_manager.load_dotenv')
@patch('os.path.exists', return_value=False)
def test_init_file_not_found(mock_load_dotenv, mock_exists):
    # Manejo de excepciones con Pytest
    with pytest.raises(FileNotFoundError, match="❌ No encuentro el archivo"):
        ConfigManager(config_path="mock_config.yaml")


@patch('src.config.config_manager.load_dotenv')
@patch('os.path.exists', return_value=True)
@patch('builtins.open', new_callable=mock_open, read_data=VALID_YAML)
@patch('os.getenv', return_value=None)  # Simulamos falta de token
def test_init_missing_jira_token(mock_load_dotenv, mock_getenv, mock_file, mock_exists):
    cfg = ConfigManager(config_path="mock_config.yaml")

    with pytest.raises(ValueError, match="❌ Falta la variable de entorno"):
        _ = cfg.jira_token