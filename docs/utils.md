# `utils.py`

## Overview

This module provides utility classes and functions to support the main functionalities of the application. Currently, it contains the `JiraFormatter` class, which is used to convert Markdown syntax to Jira's proprietary markup language.

## Classes

### `JiraFormatter`

A utility class for converting Markdown text to Jira's markup language.

#### Methods

-   **`markdown_to_jira(text: str) -> str`** (staticmethod):
    Converts a given Markdown string to the equivalent Jira markup. The method handles various Markdown elements, including:
    -   Headers (`#`, `##`, `###`)
    -   Bold text (`**text**`)
    -   Links (`[Text](url)`)
    -   Lists (`- item`)
    -   Code blocks (both inline and multi-line)

    -   **Args**:
        -   `text` (str): The Markdown string to be converted.
    -   **Returns**:
        -   `str`: The converted string in Jira markup format.
