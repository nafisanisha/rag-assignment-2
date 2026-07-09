import os
from pathlib import Path
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent


ENV_FILE = PROJECT_ROOT / ".env"
load_dotenv(ENV_FILE)


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


EMBEDDING_MODEL = os.getenv(
    "OPENAI_EMBEDDING_MODEL",
    "text-embedding-3-small"
)

CHAT_MODEL = os.getenv(
    "OPENAI_CHAT_MODEL",
    "gpt-4o-mini"
)


DOCUMENTS_FOLDER = PROJECT_ROOT / "data" / "documents"
QDRANT_FOLDER = PROJECT_ROOT / "qdrant_storage"


if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY was not found in the .env file."
    )