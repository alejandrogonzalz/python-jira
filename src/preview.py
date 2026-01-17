# src/preview.py
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel

# Asegúrate de importar tu clase existente
from core.utils import JiraFormatter

app = typer.Typer()
console = Console()


@app.command()
def convert(
    file: Path = typer.Option(
        ..., "--file", "-f", help="Ruta al archivo Markdown (.md)"
    ),
    raw: bool = typer.Option(
        False, "--raw", help="Imprimir texto plano sin formato visual"
    ),
):
    """
    Convierte un archivo Markdown a JIRA Markup y muestra el resultado.
    Útil para verificar cómo se verá antes de subirlo.
    """
    if not file.exists():
        console.print(f"[bold red]❌ Error:[/bold red] El archivo {file} no existe.")
        raise typer.Exit(code=1)

    with open(file, "r", encoding="utf-8") as f:
        content = f.read()

    # Usamos tu lógica existente
    jira_output = JiraFormatter.markdown_to_jira(content)

    console.print(Panel(f"📂 Archivo: [bold]{file.name}[/bold]", style="blue"))

    if raw:
        # Imprime tal cual (útil para copiar y pegar)
        print(jira_output)
    else:
        # Imprime con resaltado de sintaxis para que sea fácil de leer en terminal
        console.print(
            Panel(jira_output, title="Output JIRA Markup", border_style="green")
        )
        console.print("\n[dim]Tip: Usa --raw si quieres copiar el texto limpio.[/dim]")


if __name__ == "__main__":
    app()
