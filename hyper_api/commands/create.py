import typer
from pathlib import Path

app = typer.Typer()

def create_project(name: str):
    """
    Create a new FastAPI project with predefined folder structure.
    """
    project_path = Path(name)
    if project_path.exists():
        typer.echo(f"❌ Project '{name}' already exists.")
        raise typer.Exit()

    folder_structure = [
        "app",
        "app/routes",
        "app/models",
        "app/services",
        "app/utils",
        "app/core",
        "tests",
    ]

    project_path.mkdir()
    (project_path / "main.py").write_text("from app.core.app import create_app\n\napp = create_app()")

    for folder in folder_structure:
        full_path = project_path / folder
        full_path.mkdir(parents=True, exist_ok=True)
        (full_path / "__init__.py").touch()

    typer.echo(f"✅ Project '{name}' created successfully.")