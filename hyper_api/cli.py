import typer

# import all the files here
from commands import create



app = typer.Typer()


@app.command()
def generate_module(name: str):
    """
    Generate a new module
    """
    typer.echo(f"Module '{name}' generated.")

@app.command()
def generate_controller(name: str):
    """
    Generate a new controller
    """
    typer.echo(f"Controller '{name}' generated.")

@app.command()
def generate_service(name: str):
    """
    Generate a new service
    """
    typer.echo(f"Service '{name}' generated.")

@app.command()
def generate_guard(name: str):
    """
    Generate a new guard
    """
    typer.echo(f"Guard '{name}' generated.")


if __name__ == "__main__":
    app()
