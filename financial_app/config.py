"""Helpers for loading configuration for the financial planning app."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


def load_profile(path: str) -> Dict[str, Any]:
    """Load a JSON profile from disk.

    The file must contain valid JSON mapping describing the income, debt,
    and expense information required by :func:`financial_app.generate_financial_overview`.
    """

    profile_path = Path(path)
    if not profile_path.exists():
        raise FileNotFoundError(f"Profile file not found: {path}")

    with profile_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)
