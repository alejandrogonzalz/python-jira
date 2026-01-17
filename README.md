Aquí tienes el `README.md` actualizado. He reescrito la sección **"📖 Guía de Formato (Markdown)"** para explicar claramente la nueva lógica del parser (la separación entre documentación técnica e historias usando `# Historias`), y he ajustado los comandos para que usen `jira-tool`.

---

# 🚀 Jira Markdown Importer

Herramienta CLI robusta escrita en Python para automatizar la creación de **Épicas** e **Historias de Usuario** en JIRA directamente desde archivos **Markdown**.

Diseñada para equipos que prefieren documentar requerimientos en texto plano (`.md`) y sincronizarlos con JIRA sin el tedio de copiar y pegar manualmente.

## ✨ Características

* **Rich Documentation:** Soporta documentación técnica compleja en la descripción de la Épica (tablas, subtítulos, diagramas) sin confundir al parser.
* **Sección de Historias Explícita:** Usa un separador inteligente (`# Historias`) para distinguir entre documentación y tickets.
* **Format Conversion:** Traduce automáticamente negritas, listas y links de Markdown a Jira Wiki Markup.
* **Idempotencia Inteligente:** Detecta si una Épica o Historia ya existe en JIRA antes de crearla para **evitar duplicados**.
* **Modo Batch:** Procesa un archivo individual o una carpeta completa de requerimientos.
* **Seguridad:** Gestión de credenciales vía `.env` y configuración de proyectos vía `config.yaml`.
* **Modo Dry-Run:** Simula la conexión y creación de tickets para validar todo antes de tocar JIRA real.

## 🛠 Requisitos

* Python 3.9+
* [uv](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer) (Gestor de dependencias moderno)
* Una cuenta de JIRA Cloud y un [API Token](https://id.atlassian.com/manage-profile/security/api-tokens).

## 📂 Estructura del Proyecto

El proyecto sigue una arquitectura modular:

* `src/`: Código fuente.
* `main.py`: Entrada de la CLI.
* `config/`: Gestión de configuración y secretos.
* `core/`: Lógica de negocio (Adapter, Parser).


* `config.yaml`: Mapeo de alias de proyectos (ej: `MERIDIAN` -> `MT`).
* `pyproject.toml`: Definición de dependencias y herramientas.

## 🚀 Instalación y Configuración

1. **Instalar dependencias:**
```sh
uv sync

```


2. **Configurar credenciales:**
Crea un fichero `.env` en la raíz con tu token (no lo compartas):
```env
JIRA_API_TOKEN="tu_token_de_atlassian_aqui"

```


3. **Configurar proyectos:**
Edita `config.yaml` para definir tus alias:
```yaml
jira:
  url: "https://tu-dominio.atlassian.net"
  email: "tu-email@ejemplo.com"
projects:
  MERIDIAN:
    key: "MT" # La Key real del proyecto en Jira

```



## 📖 Guía de Formato (Markdown)

La herramienta utiliza la estrategia **"Un archivo = Una Épica"**.
El parser busca un separador específico (`# Historias`) para dividir el archivo en dos secciones lógicas:

1. **Arriba del separador:** Descripción de la Épica (Soporta formato rico, subtítulos `##`, tablas, etc.).
2. **Abajo del separador:** Historias de Usuario (Cada `##` se convierte en un ticket).

### Ejemplo de Archivo (`01-arquitectura.md`)

```markdown
# Título de la Épica (Se convierte en Epic)

Esta sección es la **Descripción**. Puedes usar formato libre.

## 🛠 Detalles Técnicos (Se mantiene en la descripción)
- Puedes usar subtítulos aquí para documentar arquitectura.
- Esto NO creará historias nuevas.

---
# Historias

## Título de la Historia 1 (Se convierte en Story)
Como usuario quiero...

**Criterios de Aceptación:**
- El sistema debe validar X.

## Título de la Historia 2
Descripción de la segunda historia...

```

**Nota:** Si olvidas poner `# Historias`, todo el contenido se considerará parte de la descripción de la Épica y no se crearán historias hijas.

## 💻 Comandos de Ejecución

Puedes ejecutar la herramienta apuntando a un solo archivo o a una carpeta entera.

### 1. Modo Prueba (Dry-Run)

*Recomendado siempre antes de subir cambios.* Verifica conexión, valida el markdown y busca duplicados en Jira sin crear nada.

```sh
uv run jira-tool create --file ./requerimientos --project MERIDIAN --dry-run

```

### 2. Procesar un Archivo Único

```sh
uv run jira-tool create --file ./requerimientos/01-login.md --project MERIDIAN

```

---

## 🧹 Calidad de Código y Mantenimiento

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

* **[Adapter](https://www.google.com/search?q=./docs/adapter.md)**: Lógica de conexión, manejo de errores y sistema anti-duplicados.
* **[Parser](https://www.google.com/search?q=./docs/parser.md)**: Reglas de transformación Regex y lógica de separación por secciones.