import typer
from pathlib import Path
import subprocess

def run_tests():
    """
    Run tests in the 'tests' directory using pytest.
    """
    tests_path = Path("tests")
    if not tests_path.exists():
        typer.echo("❌ No 'tests' directory found.")
        raise typer.Exit()

    typer.echo("🧪 Running tests...")
    try:
        subprocess.run(["pytest", "tests"], check=True)
        typer.echo("✅ Tests completed.")
    except subprocess.CalledProcessError:
        typer.echo("❌ Some tests failed.")