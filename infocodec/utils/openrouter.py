"""
OpenRouter API key resolution and client factory.

Resolution order for OPENROUTER_API_KEY:
  1. .env file at the project root   (loaded via python-dotenv)
  2. Environment variable             (os.environ)
  3. Raises OpenRouterKeyError with a clear remediation message

Usage:
    from infocodec.utils.openrouter import get_api_key, get_client

    key = get_api_key()          # raises if unresolved
    client = get_client()        # raises if unresolved
"""

import os
from pathlib import Path

from dotenv import dotenv_values


# Sentinel value written into .env.example — treated as "not configured"
_PLACEHOLDER = "your-api-key-here"


class OpenRouterKeyError(RuntimeError):
    """Raised when OPENROUTER_API_KEY cannot be resolved from any source."""


def _find_dotenv() -> Path | None:
    """Walk up from the package root to find the nearest .env file."""
    candidate = Path(__file__).resolve().parent
    while candidate != candidate.parent:
        env_file = candidate / ".env"
        if env_file.is_file():
            return env_file
        # Stop at the project root (where pyproject.toml lives)
        if (candidate / "pyproject.toml").is_file():
            break
        candidate = candidate.parent
    return None


def get_api_key() -> str:
    """
    Resolve OPENROUTER_API_KEY using a two-step fallback chain.

    1. Read the project-root .env file (via dotenv_values — does NOT mutate
       os.environ, so repeated calls are idempotent).
    2. Check os.environ (covers shell exports, Docker secrets, CI variables, etc.)

    Returns:
        The API key string (non-empty, non-placeholder).

    Raises:
        OpenRouterKeyError: if the key is absent or still set to the placeholder
            value in both sources, with a message explaining how to fix it.
    """
    # --- Step 1: .env file ---
    env_file = _find_dotenv()
    if env_file is not None:
        dot_env_values = dotenv_values(env_file)
        key_from_file = (dot_env_values.get("OPENROUTER_API_KEY") or "").strip()
        if key_from_file and key_from_file != _PLACEHOLDER:
            return key_from_file

    # --- Step 2: environment variable ---
    key_from_env = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if key_from_env and key_from_env != _PLACEHOLDER:
        return key_from_env

    # --- Step 3: fail with a helpful message ---
    env_path = env_file or Path("<project-root>/.env")
    raise OpenRouterKeyError(
        "OPENROUTER_API_KEY is not configured.\n\n"
        "Tried:\n"
        f"  1. {env_path}  →  key missing or still set to placeholder\n"
        "  2. os.environ['OPENROUTER_API_KEY']  →  not set\n\n"
        "Fix (choose one):\n"
        f"  • Edit {env_path} and set:  OPENROUTER_API_KEY=sk-or-...\n"
        "  • Export in your shell:     export OPENROUTER_API_KEY=sk-or-...\n"
        "  • Enter it in the Settings page of the Streamlit UI\n\n"
        "Get a key at: https://openrouter.ai/keys"
    )


def get_client(api_key: str | None = None):
    """
    Return an OpenAI-compatible client pointed at OpenRouter.

    Args:
        api_key: Override the resolved key. If None, calls get_api_key().

    Returns:
        openai.OpenAI instance configured for OpenRouter.

    Raises:
        OpenRouterKeyError: if api_key is None and the key cannot be resolved.
    """
    from openai import OpenAI  # lazy import — openai is an optional heavy dep

    resolved_key = api_key if api_key else get_api_key()
    return OpenAI(
        api_key=resolved_key,
        base_url="https://openrouter.ai/api/v1",
    )
