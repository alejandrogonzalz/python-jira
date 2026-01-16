import typer
from rich.console import Console
from rich.panel import Panel
from src import ConfigManager
from src import JiraAdapter
from src import MarkdownParser

# Inicializamos la app y la consola para prints bonitos
app = typer.Typer()
console = Console()

@app.command()
def create(
    file: str = typer.Option(..., "--file", "-f", help="Ruta al archivo Markdown (.md)"),
    project: str = typer.Option(..., "--project", "-p", help="Alias del proyecto definido en config.yaml"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Simula la ejecución sin crear tickets reales")
):
    """
    Lee un archivo Markdown y crea Épicas e Historias en JIRA.
    """
    try:
        # 1. Cargar Configuración
        cfg = ConfigManager()
        
        # 2. Inicializar Adaptador
        if dry_run:
            console.print(Panel("⚠️ MODO DRY-RUN: No se crearán tickets reales", style="yellow"))
            
        jira = JiraAdapter(
            url=cfg.jira_url,
            email=cfg.jira_email,
            token=cfg.jira_token,
            dry_run=dry_run
        )

        # 3. Validar Proyecto
        project_key = cfg.get_project_key(project)
        console.print(f"[bold green]🚀 Conectado a:[/bold green] {cfg.jira_url}")
        console.print(f"[bold green]📂 Proyecto:[/bold green] {project_key}")

        # 4. Parsear Archivo
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
        
        parser = MarkdownParser()
        epics = parser.parse(content)
        
        console.print(f"📝 Se encontraron [bold cyan]{len(epics)}[/bold cyan] épicas.")

        # 5. Ejecución
        for epic in epics:
            console.print(f"\nProcesando Épica: [bold]{epic.title}[/bold]...")
            epic_key = jira.create_epic(project_key, epic)
            
            if epic_key:
                for story in epic.stories:
                    jira.create_story(project_key, epic_key, story)

        console.print("\n[bold green]✅ ¡Proceso finalizado con éxito![/bold green]")

    except Exception as e:
        console.print(f"[bold red]❌ Error Fatal:[/bold red] {e}")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()