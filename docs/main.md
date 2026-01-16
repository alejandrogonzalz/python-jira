# `main.py`

## Overview

This is the main entry point of the application. It uses the `typer` library to create a command-line interface (CLI) that allows users to create Jira Epics and Stories from a Markdown file.

## CLI Commands

### `create`

Reads a Markdown file and creates Epics and User Stories in Jira based on its content.

-   **Usage**:
    ```sh
    python -m src.main create --file <path_to_markdown_file> --project <project_alias> [--dry-run]
    ```

-   **Options**:
    -   `--file`, `-f` (str): The path to the input Markdown file. This is a required option.
    -   `--project`, `-p` (str): The alias of the Jira project, as defined in the `config.yaml` file. This is a required option.
    -   `--dry-run` (bool): If set, the application will simulate the creation process without making any actual changes in Jira. This is useful for testing and validation. Defaults to `False`.

## Execution Flow

1.  **Load Configuration**: Initializes the `ConfigManager` to load the application settings.
2.  **Initialize Jira Adapter**: Creates an instance of the `JiraAdapter`, which handles communication with the Jira API. If `--dry-run` is specified, the adapter is set to simulation mode.
3.  **Validate Project**: Retrieves the Jira project key using the provided alias.
4.  **Parse Markdown**: Reads the content of the specified Markdown file and uses the `MarkdownParser` to extract a list of Epics and their associated User Stories.
5.  **Create Jira Issues**:
    -   Iterates through the parsed Epics and calls `jira.create_epic()` to create each one in Jira.
    -   If an Epic is created successfully, it then iterates through its User Stories and calls `jira.create_story()` to create each story and link it to the parent Epic.
6.  **Error Handling**: Catches and reports any exceptions that occur during the process.

## Example

```sh
python -m src.main create --file ./my_project_epics.md --project tienda --dry-run
```
