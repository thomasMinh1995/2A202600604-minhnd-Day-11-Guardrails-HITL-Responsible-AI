"""
Lab 11 — Configuration & API Key Setup
"""
import os
import sys


def setup_api_key(required: bool = True) -> bool:
    """Load Google API key from environment or prompt.

    Args:
        required: If True, raise an error when no API key is available in a
            non-interactive session. If False, quietly skip loading.

    Returns:
        True when a key is available, otherwise False.
    """
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "0"

    if os.environ.get("GOOGLE_API_KEY"):
        print("API key loaded.")
        return True

    if not required:
        print("GOOGLE_API_KEY not set. Skipping API-dependent setup.")
        return False

    if sys.stdin.isatty():
        os.environ["GOOGLE_API_KEY"] = input("Enter Google API Key: ").strip()
        if os.environ["GOOGLE_API_KEY"]:
            print("API key loaded.")
            return True

    raise RuntimeError(
        "GOOGLE_API_KEY is required for this part. Export it first, for example: "
        "export GOOGLE_API_KEY='your-api-key-here'"
    )


# Allowed banking topics (used by topic_filter)
ALLOWED_TOPICS = [
    "banking", "account", "transaction", "transfer",
    "loan", "interest", "savings", "credit",
    "deposit", "withdrawal", "balance", "payment",
    "tai khoan", "giao dich", "tiet kiem", "lai suat",
    "chuyen tien", "the tin dung", "so du", "vay",
    "ngan hang", "atm",
]

# Blocked topics (immediate reject)
BLOCKED_TOPICS = [
    "hack", "exploit", "weapon", "drug", "illegal",
    "violence", "gambling", "bomb", "kill", "steal",
]
