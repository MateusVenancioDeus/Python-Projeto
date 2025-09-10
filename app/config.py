from dotenv import load_dotenv
from pathlib import Path


def load_environment():
    root = Path(__file__).resolve().parent.parent
    env_path = root / ".env"
    load_dotenv(dotenv_path=env_path)
