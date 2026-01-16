# `adapter.py`

## Overview

This module provides the `JiraAdapter` class, which acts as an interface to the Jira API. It is responsible for creating Epics and User Stories in Jira. The adapter is implemented as a singleton to ensure a single, consistent connection to the Jira instance.

## Classes

### `JiraAdapter`

A singleton adapter class for interacting with the Jira API. This class provides methods for creating Epics and User Stories in Jira.

#### `__new__(cls, *args, **kwargs)`

Implements the singleton pattern, ensuring that only one instance of `JiraAdapter` is created.

#### `__init__(self, url: str, email: str, token: str, dry_run: bool = False)`

Initializes the `JiraAdapter` and establishes a connection to the Jira instance if one does not already exist.

-   **Args**:
    -   `url` (str): The URL of the Jira instance.
    -   `email` (str): The email of the user to authenticate with.
    -   `token` (str): The API token for authentication.
    -   `dry_run` (bool): If `True`, the adapter will simulate API calls without making any actual changes in Jira. Defaults to `False`.
-   **Raises**:
    -   `ConnectionError`: If the connection to Jira fails.

#### Methods

-   **`create_epic(self, project_key: str, epic: Epic) -> Optional[str]`**:
    Creates an Epic in Jira.

    -   **Args**:
        -   `project_key` (str): The key of the Jira project where the Epic will be created.
        -   `epic` (Epic): An `Epic` object containing the details of the epic to be created.
    -   **Returns**:
        -   `Optional[str]`: The key of the newly created Epic (e.g., 'PROJ-10'), or `None` if the creation fails.

-   **`create_story(self, project_key: str, parent_epic_key: str, story: UserStory)`**:
    Creates a User Story in Jira and links it to a parent Epic.

    -   **Args**:
        -   `project_key` (str): The key of the Jira project where the story will be created.
        -   `parent_epic_key` (str): The key of the parent Epic to which the story will be linked.
        -   `story` (UserStory): A `UserStory` object containing the details of the story to be created.
