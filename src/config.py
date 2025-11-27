# src/config.py

"""
Central place to load configuration from environment variables (.env).

We use python-dotenv to load .env file in development.

Important:
- Never commit real API keys to GitHub.
"""

import os
from dotenv import load_dotenv

# Load .env file if present
load_dotenv()

# Which provider to use, e.g. 'gemini', 'openai'
LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "gemini")

# Real API key (if you ever set it)
LLM_API_KEY: str | None = os.getenv("LLM_API_KEY")

# Whether to use Fake LLM (default: True for safety)
USE_FAKE_LLM: bool = os.getenv("USE_FAKE_LLM", "true").lower() == "true"
