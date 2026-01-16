# `parser.py`

## Overview

This module is responsible for parsing Markdown content to extract project management items like Epics and User Stories. It defines the data structures for these items and contains the logic for parsing a Markdown string into a structured format.

## Classes

### `UserStory`

A data class representing a User Story.

-   **Attributes**:
    -   `title` (str): The title of the User Story.
    -   `description` (str): The description of the User Story.
    -   `acceptance_criteria` (List[str]): A list of acceptance criteria for the User Story.

-   **Methods**:
    -   **`add_line(self, line: str)`**: Adds a line of text to the User Story. It automatically detects whether the line is part of the description or an acceptance criterion based on its formatting (lines starting with "- " are treated as acceptance criteria).

### `Epic`

A data class representing an Epic.

-   **Attributes**:
    -   `title` (str): The title of the Epic.
    -   `description` (str): The description of the Epic.
    -   `stories` (List[UserStory]): A list of `UserStory` objects associated with the Epic.

-   **Methods**:
    -   **`add_line(self, line: str)`**: Adds a line of text to the Epic's description.

### `MarkdownParser`

A class that parses a Markdown string to extract a list of Epics and their associated User Stories.

#### `__init__(self)`

Initializes the `MarkdownParser`, which compiles regular expressions for detecting Epic and User Story titles in the Markdown content.

#### `parse(self, content: str) -> List[Epic]`

Parses the given Markdown content and returns a list of `Epic` objects.

-   **Args**:
        -   `content` (str): The Markdown content to be parsed.
-   **Returns**:
        -   `List[Epic]`: A list of `Epic` objects extracted from the content.
-   **Raises**:
        -   `ValueError`: If a User Story is found without a parent Epic.
