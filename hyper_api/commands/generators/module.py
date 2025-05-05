import typer
from pathlib import Path

def create_module(name: str):
    """
    Create a new module folder with standard FastAPI files inside.
    Example: src/app/user/{all_files}
    """
    module_path = Path(f"src/app/{name}")
    test_path = Path(f"tests/{name}")

    if module_path.exists():
        typer.echo(f"❌ Module '{name}' already exists.")
        raise typer.Exit()

    # Files to create inside the module folder
    files = {
        f"{module_path}/__init__.py": "",
        f"{module_path}/routes.py": f"# FastAPI {name} routes",
        f"{module_path}/models.py": f"# {name.capitalize()} domain models",
        f"{module_path}/service.py": f"# {name.capitalize()} service logic",
        f"{module_path}/repository.py": f"# {name.capitalize()} repository for DB access",
        f"{module_path}/schemas.py": f"# Pydantic {name} schemas",
        f"{module_path}/deps.py": f"# Dependency injection for {name} module",
        f"{test_path}/test_{name}.py": f"# Test for {name} module",
    }

    # Create folders and files
    for file, content in files.items():
        path = Path(file)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        typer.echo(f"✅ Created file: {path}")

    typer.echo(f"✅ Module '{name}' created successfully.")
