import typer
from commands.create import create_project
from commands.generators.module import create_module

app = typer.Typer()

@app.command()
def create(name: str):
    """
    Create a new project with the given name.
    """
    create_project(name)
    
@app.command()
def res(name: str):
    """
    Create a new project with the given name.
    """
    create_module(name)

if __name__ == "__main__":
    app()
