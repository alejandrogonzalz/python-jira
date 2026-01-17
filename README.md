Aquí tienes el `README.md` actualizado. He integrado las nuevas funcionalidades que programamos (soporte para carpetas, sistema anti-duplicados) y la sección de mantenimiento con `ruff` tal como pediste.

Está listo para copiar y pegar.

# 🚀 Jira Markdown Importer

Herramienta CLI robusta escrita en Python para automatizar la creación de **Épicas** e **Historias de Usuario** en JIRA directamente desde archivos **Markdown**.

Diseñada para equipos que prefieren documentar requerimientos en texto plano (`.md`) y sincronizarlos con JIRA sin el tedio de copiar y pegar manualmente.

## ✨ Características

- **Markdown Parsing:** Convierte `# Títulos` en Épicas y `## Subtítulos` en Historias.
- **Formato Rico:** Traduce automáticamente negritas, listas y links de Markdown a Jira Wiki Markup.
- **Idempotencia Inteligente:** Detecta si una Épica o Historia ya existe en JIRA antes de crearla para **evitar duplicados**.
- **Modo Batch:** Procesa un archivo individual o una carpeta completa de requerimientos.
- **Configuración Segura:** Gestión de credenciales vía `.env` y configuración de proyectos vía `config.yaml`.
- **Modo Dry-Run:** Simula la conexión y creación de tickets para validar todo antes de tocar JIRA real.

## 🛠 Requisitos

- Python 3.9+
- [uv](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer) (Gestor de dependencias moderno)
- Una cuenta de JIRA Cloud y un [API Token](https://id.atlassian.com/manage-profile/security/api-tokens).

## 📂 Estructura del Proyecto

El proyecto sigue una arquitectura modular:

-   `src/`: Código fuente.
    -   `main.py`: Entrada de la CLI.
    -   `config/`: Gestión de configuración y secretos.
    -   `core/`: Lógica de negocio (Adapter, Parser).
-   `config.yaml`: Mapeo de alias de proyectos (ej: `t9` -> `MT`).
-   `pyproject.toml`: Definición de dependencias y herramientas.

## 🚀 Instalación y Configuración

1.  **Instalar dependencias:**
    ```sh
    uv sync
    ```

2.  **Configurar credenciales:**
    Crea un fichero `.env` en la raíz con tu token (no lo compartas):
    ```env
    JIRA_API_TOKEN="tu_token_de_atlassian_aqui"
    ```

3.  **Configurar proyectos:**
    Edita `config.yaml` para definir tus alias:
    ```yaml
    jira:
      url: "[https://tu-dominio.atlassian.net](https://tu-dominio.atlassian.net)"
      email: "tu-email@ejemplo.com"
    projects:
      t9:
        key: "MT" # La Key real del proyecto en Jira
    ```

## 📖 Guía de Uso (Markdowns)

Recomendamos encarecidamente la estrategia **"Un archivo, una Épica"**. Esto mantiene la documentación ordenada y facilita el seguimiento.

**Estructura recomendada de archivos:**
```text
/requerimientos
  ├── 01-autenticacion.md
  ├── 02-panel-control.md
  └── 03-reportes.md

```

**Formato dentro del Markdown (.md):**

```markdown
# Título de la Épica (Se convierte en Epic)
Descripción general de alto nivel de la funcionalidad.

## Título de la Historia (Se convierte en Story)
Como usuario quiero...

**Criterios de Aceptación:**
- El sistema debe validar X.
- El usuario debe ver Y.

```

## 💻 Comandos de Ejecución

Puedes ejecutar la herramienta apuntando a un solo archivo o a una carpeta entera.

### 1. Modo Prueba (Dry-Run)

*Recomendado siempre antes de subir cambios.* Verifica conexión y duplicados sin crear nada.

```sh
uv run jira-tool create --file ./data --project MERIDIAN --dry-run

```

### 2. Procesar un Archivo Único

```sh
uv run jira-tool --file ./epics/01-login.md --project MERIDIAN

```

---

## 🧹 Calidad de Código y Desarrollo

Utilizamos **Ruff** para mantener el código limpio, formateado y con los imports ordenados.

**Formatear automáticamente todo el código:**

```sh
uvx ruff format .

```

**Chequear errores y ordenar imports (Sort Imports):**

```sh
uvx ruff check --select I --fix .

```

## Documentación Técnica

La documentación detallada de módulos se encuentra en `docs/`:

* **[Adapter](https://www.google.com/search?q=./docs/adapter.md)**: Lógica de conexión y anti-duplicados.
* **[Parser](https://www.google.com/search?q=./docs/parser.md)**: Reglas de transformación Markdown -> Jira.
