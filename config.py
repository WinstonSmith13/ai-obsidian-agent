import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
VAULT_PATH = os.getenv("VAULT_PATH")

if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY is not set")
if not VAULT_PATH:
    raise ValueError("VAULT_PATH is not set")