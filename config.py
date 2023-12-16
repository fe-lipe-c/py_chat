from pathlib import Path
import os

DATA_PATH = Path("__file__").parent / "data"
REFERENCE_PATH = DATA_PATH / "reference"
CHATS_PATH = DATA_PATH / "chats"

# Create folders if they don't exist.
Path.mkdir(DATA_PATH, parents=True, exist_ok=True)
Path.mkdir(REFERENCE_PATH, parents=True, exist_ok=True)
Path.mkdir(CHATS_PATH, parents=True, exist_ok=True)

# Create file 'chats_st.json' if it doesn't exist.
CHATS_SAVE_FILE = CHATS_PATH / "chats_st.json"

# Load 'participantes' data.

OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
