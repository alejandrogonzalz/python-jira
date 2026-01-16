# `config_manager.py`

## Overview

This module provides the `ConfigManager` class, responsible for managing the application's configuration. It loads settings from a `config.yaml` file and retrieves sensitive information, like the Jira API token, from environment variables.

## Classes

### `ConfigManager`

Manages configuration for the Jira integration. It loads configuration from a YAML file and environment variables.

#### `__init__(self, config_path: str = "config.yaml")`

Initializes the `ConfigManager`.

-   **Args**:
    -   `config_path` (str): The path to the configuration YAML file. Defaults to "config.yaml".
-   **Raises**:
    -   `FileNotFoundError`: If the specified `config_path` does not exist.

#### Properties

-   **`jira_url`** (str): Returns the Jira URL from the configuration.
-   **`jira_email`** (str): Returns the Jira user email from the configuration.
-   **`jira_token`** (str): Returns the Jira API token from the `JIRA_API_TOKEN` environment variable.
    -   **Raises**:
        -   `ValueError`: If the `JIRA_API_TOKEN` environment variable is not set.

#### Methods

-   **`get_project_key(self, alias: str) -> str`**:
    Retrieves the actual Jira project key (e.g., 'ECOMM') given a project alias (e.g., 'tienda').
    -   **Args**:
        -   `alias` (str): The project alias defined in the `config.yaml` file.
    -   **Returns**:
        -   `str`: The corresponding Jira project key.
    -   **Raises**:
        -   `ValueError`: If the provided alias is not defined in the configuration file.
