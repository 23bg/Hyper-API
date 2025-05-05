import typer
from pathlib import Path


def create_project(name: str):
    """
    Create a new FastAPI project with a predefined folder structure.
    """
    project_path = Path(name)
    if project_path.exists():
        typer.echo(f"❌ Project '{name}' already exists.")
        raise typer.Exit()

    # Define base folders
    folders = [
        "src",
        "src/app",
        "src/core",
        "src/utils",
        "src/core/database",
        "src/admin",
        "src/admin/templates",
        "src/admin/static",
        # Test Files
        "tests",
    ]

    # Define specific files to create inside each folder
    files = {
        "src/main.py": """from app.core.app import create_app

app = create_app()""",
        # Admin panel files
        "src/admin/template.py": """# Admin panel configuration file
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_admin_dashboard():
    return {"message": "Welcome to the Admin Dashboard!"}
""",
        "src/admin/templates/index.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Dashboard</title>
    <link rel="stylesheet" href="{{ url_for('static', path='css/style.css') }}">
</head>
<body>
    <h1>Admin Dashboard</h1>
    <p>Welcome to the Admin Panel!</p>
    <a href="/admin/login">Login</a>
</body>
</html>""",
        "src/admin/templates/auth/login.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Login</title>
    <link rel="stylesheet" href="{{ url_for('static', path='css/style.css') }}">
</head>
<body>
    <h1>Login to Admin Panel</h1>
    <form action="/admin/login" method="post">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" required><br>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required><br>
        <button type="submit">Login</button>
    </form>
</body>
</html>""",
        # Core files
        "src/core/config.py": """# Configuration file
from pydantic import BaseSettings

class Settings(BaseSettings):
    project_name: str = "Admin Panel"
    admin_email: str = "admin@example.com"
    database_url: str = "sqlite:///./test.db"  # SQLite DB URL
    secret_key: str = "mysecretkey"  # Example secret key for JWT

    class Config:
        env_file = ".env"

settings = Settings()""",
        "src/core/database/sqlite.py": """# SQLite Database configuration
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..config import settings

DATABASE_URL = settings.database_url
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
""",
        "src/core/database/mongodb.py": """# MongoDB Database configuration
import motor.motor_asyncio
from ..config import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.database_url)
db = client.get_database()

# Example MongoDB collection
users_collection = db.users
""",
        "src/core/security.py": """# Security utilities
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
""",
        # Utility files
        "src/utils/logger_utils.py": """# Logger utility
import logging

logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)

def log_message(message: str):
    logger.info(message)

def log_error(error: str):
    logger.error(error)
""",
        # User module files
        "src/app/user/user_routes.py": """# FastAPI user routes
from fastapi import APIRouter
from . import user_service

router = APIRouter()

@router.post("/register")
async def register_user(user: dict):
    return await user_service.register_user(user)

@router.get("/users/{user_id}")
async def get_user(user_id: int):
    return await user_service.get_user(user_id)
""",
        "src/app/user/models.py": """# User domain models
from sqlalchemy import Column, Integer, String
from src.core.database.sqlite import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, unique=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
""",
        "src/app/user/user_service.py": """# User service logic
from .models import User
from src.core.database.sqlite import SessionLocal
from src.core.security import hash_password
from sqlalchemy.orm import Session

def register_user(user: dict, db: Session):
    db_user = User(username=user["username"], email=user["email"], hashed_password=hash_password(user["password"]))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(user_id: int, db: Session):
    return db.query(User).filter(User.id == user_id).first()
""",
        "src/app/user/user_repository.py": """# User repository for DB access
from sqlalchemy.orm import Session
from .models import User

def get_user_by_id(user_id: int, db: Session):
    return db.query(User).filter(User.id == user_id).first()
""",
        "src/app/user/user_schema.py": """# Pydantic user schemas
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True
""",
        "src/app/user/deps.py": """# Dependency injection for user module
from sqlalchemy.orm import Session
from src.core.database.sqlite import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
""",
        # Tests for user module
        "tests/user/test_user.py": """# Test for user module
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_register_user():
    response = client.post("/register", json={"username": "testuser", "email": "test@example.com", "password": "password"})
    assert response.status_code == 200
    assert "username" in response.json()

def test_get_user():
    response = client.get("/users/1")
    assert response.status_code == 200
    assert "username" in response.json()
""",
    }

    # Create project root
    project_path.mkdir()

    # Create folders and __init__.py files
    for folder in folders:
        full_path = project_path / folder
        full_path.mkdir(parents=True, exist_ok=True)
        (full_path / "__init__.py").touch()

    # Create files with content
    for file_path, content in files.items():
        file_full_path = project_path / file_path
        file_full_path.parent.mkdir(parents=True, exist_ok=True)
        file_full_path.write_text(content)

    # Create .gitignore
    gitignore_content = """
    # Python
    *.pyc
    __pycache__/
    .pytest_cache/
    
    # FastAPI
    .env
    .vscode/
    .mypy_cache/
    .coverage
    """
    (project_path / ".gitignore").write_text(gitignore_content)

    # Create README.md
    readme_content = f"# {name}\n\nA FastAPI project."
    (project_path / "README.md").write_text(readme_content)

    # Create pyproject.toml
    pyproject_content = """
    [tool.poetry]
    name = "{name}"
    version = "0.1.0"
    description = "A FastAPI project"
    authors = ["Your Name <youremail@example.com>"]
    
    [tool.poetry.dependencies]
    python = "^3.9"
    fastapi = "^0.75.0"
    uvicorn = "^0.17.0"

    [tool.poetry.dev-dependencies]
    black = "^21.9b0"
    flake8 = "^4.0.0"
    """
    (project_path / "pyproject.toml").write_text(pyproject_content.format(name=name))

    # Create Dockerfile
    dockerfile_content = """
    # Use an official Python runtime as a parent image
    FROM python:3.9-slim

    # Set the working directory inside the container
    WORKDIR /usr/src/app

    # Copy the current directory contents into the container at /usr/src/app
    COPY . .

    # Install dependencies
    RUN pip install --no-cache-dir -r requirements.txt

    # Expose the port the app runs on
    EXPOSE 8000

    # Define environment variables (optional)
    ENV PYTHONUNBUFFERED 1

    # Command to run the app with Uvicorn
    CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
    """
    (project_path / "Dockerfile").write_text(dockerfile_content)

    # Create Commitizen config
    commitizen_content = """
    # .cz.yaml
    name: "cz-conventional-changelog"
    version: "3.1.0"
    tagPrefix: ""
    """
    (project_path / ".cz.yaml").write_text(commitizen_content)

    # Create Python linter configuration (flake8)
    flake8_content = """
    [flake8]
    max-line-length = 88
    """
    (project_path / ".flake8").write_text(flake8_content)

    # Create Python linter configuration (flake8)
    env_local = """
    [flake8]
    max-line-length = 88
    """
    (project_path / ".env.local").write_text(env_local)

    # Create Python linter configuration (flake8)
    env_test = """
    [flake8]
    max-line-length = 88
    """
    (project_path / ".env.test").write_text(env_test)

    # Create Python linter configuration (flake8)
    env_release = """
    [flake8]
    max-line-length = 88
    """
    (project_path / ".env.release").write_text(env_release)

    # Create tox.ini for testing and linting (optional)
    tox_content = """
    [tox]
    envlist = py38, lint

    [testenv:lint]
    description = run linters
    deps = flake8
    commands = flake8 src tests

    [testenv]
    deps = pytest
    commands = pytest
    """
    (project_path / "tox.ini").write_text(tox_content)

    typer.echo(f"✅ Project '{name}' created successfully.")
