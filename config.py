from pathlib import Path
import pandas as pd
import os

CHAT_PATH = Path("__file__").parent / "chat"
# REFERENCE_PATH = DATA_PATH / "reference"

# Create folders if they don't exist.
Path.mkdir(CHAT_PATH, parents=True, exist_ok=True)

# Load 'participantes' data.

OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
