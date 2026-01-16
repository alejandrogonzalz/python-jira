# 🚀 Jira Markdown Importer

Herramienta CLI robusta escrita en Python para automatizar la creación de **Épicas** e **Historias de Usuario** en JIRA directamente desde archivos **Markdown**.

Diseñada para equipos que prefieren documentar requerimientos en texto plano (`.md`) y sincronizarlos con JIRA sin el tedio de copiar y pegar manualmente.

## ✨ Características

- **Markdown Parsing:** Convierte `# Títulos` en Épicas y `## Subtítulos` en Historias.
- **Formato Rico:** Traduce automáticamente negritas, listas y links de Markdown a Jira Wiki Markup.
- **Configuración Segura:** Gestión de credenciales vía `.env` y configuración de proyectos vía `config.yaml`.
- **Modo Dry-Run:** Simula la creación de tickets para validar el contenido antes de ensuciar JIRA.
- **Auto-Discovery:** Detecta automáticamente los IDs de campos personalizados (como "Epic Name").

## 🛠 Requisitos

- Python 3.9+
- [uv](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer) (Gestor de dependencias recomendado)
- Una cuenta de JIRA Cloud y un [API Token](https://id.atlassian.com/manage-profile/security/api-tokens).

