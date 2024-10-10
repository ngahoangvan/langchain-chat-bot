from pathlib import Path


# API
VERSION = "v1"
API_PREFIX = f"/api/{VERSION}"

DB_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}

BASE_DIR = Path(__file__).resolve().parent.parent

# OpenAI
DEFAULT_OPENAI_MODEL = "gpt-4o"
DEFAULT_OPENAI_REQUEST_TIMEOUT = 25

# Embedding Models
EMBEDDING_3_DIMENSIONS = 1024
