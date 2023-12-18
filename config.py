from pathlib import Path
import json
import os
from qdrant_client import QdrantClient

DATA_PATH = Path("__file__").parent / "data"
REFERENCE_PATH = DATA_PATH / "reference"
CHATS_PATH = DATA_PATH / "chats"

# Create folders if they don't exist.
Path.mkdir(DATA_PATH, parents=True, exist_ok=True)
Path.mkdir(REFERENCE_PATH, parents=True, exist_ok=True)
Path.mkdir(CHATS_PATH, parents=True, exist_ok=True)

# Create file 'chats_st.json' if it doesn't exist.
CHATS_SAVE_FILE = CHATS_PATH / "chats_st.json"

# Qdrant client setup
QDRANT_DB_CLIENT = QdrantClient(host="localhost", port=6333)

# Load openai models list
with open(REFERENCE_PATH / "openai_models.json", "r") as f:
    OPENAI_MODELS = json.load(f)

# OpenAI API key
OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
