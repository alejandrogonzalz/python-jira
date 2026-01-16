# 🚀 Jira Markdown Importer

Herramienta CLI robusta escrita en Python para automatizar la creación de **Épicas** e **Historias de Usuario** en JIRA directamente desde archivos **Markdown**.

Diseñada para equipos que prefieren documentar requerimientos en texto plano (`.md`) y sincronizarlos con JIRA sin el tedio de copiar y pegar manualmente.

## Características

- **Markdown Parsing:** Convierte `# Títulos` en Épicas y `## Subtítulos` en Historias.
- **Formato Rico:** Traduce automáticamente negritas, listas y links de Markdown a Jira Wiki Markup.
- **Configuración Segura:** Gestión de credenciales vía `.env` y configuración de proyectos vía `config.yaml`.
- **Modo Dry-Run:** Simula la creación de tickets para validar el contenido antes de ensuciar JIRA.
- **Auto-Discovery:** Detecta automáticamente los IDs de campos personalizados (como "Epic Name").

## 🛠 Requisitos

- Python 3.9+
- [uv](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer) (Gestor de dependencias recomendado)
- Una cuenta de JIRA Cloud y un [API Token](https://id.atlassian.com/manage-profile/security/api-tokens).

## Estructura del Proyecto

El proyecto está organizado de la siguiente manera:

-   `src/`: Contiene el código fuente de la aplicación.
    -   `main.py`: El punto de entrada de la aplicación CLI.
    -   `config/`: Módulo para la gestión de la configuración.
    -   `core/`: Contiene la lógica principal de la aplicación (parser, adaptador de Jira, etc.).
-   `docs/`: Contiene la documentación detallada del proyecto.
-   `tests/`: Contiene los tests unitarios.
-   `config.yaml`: Fichero de configuración de proyectos.
-   `pyproject.toml`: Fichero de definición del proyecto y dependencias.

## Documentación

La documentación detallada de cada módulo se encuentra en el directorio `docs/`:

-   [**`main.py`**](./docs/main.md): Documentación del punto de entrada de la CLI.
-   [**`config_manager.py`**](./docs/config_manager.md): Documentación del gestor de configuración.
-   [**`adapter.py`**](./docs/adapter.md): Documentación del adaptador de Jira.
-   [**`parser.py`**](./docs/parser.md): Documentación del parser de Markdown.
-   [**`utils.py`**](./docs/utils.md): Documentación de las utilidades.

## Uso

1.  **Instalar dependencias:**
    ```sh
    uv sync
    ```

2.  **Configurar el proyecto:**
    -   Crea un fichero `.env` en la raíz del proyecto con tu token de Jira:
        ```
        JIRA_API_TOKEN="tu_token_de_api"
        ```
    -   Configura tus proyectos en `config.yaml`.

3.  **Ejecutar la aplicación:**
    ```sh
    uv run jira-tool create --file <ruta_al_fichero.md> --project <alias_del_proyecto>
    ```

    -   **Ejemplo con dry-run:**
        ```sh
        uv run jira-tool create --file ejemplos/epicas.md --project tienda --dry-run
        ```
