#!/usr/bin/env python3
"""
Minimal local smoke test for the Railway backend deployment shape.
It boots the Flask app with production-like env vars and verifies /health.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BACKEND_DIR = ROOT / "backend"


def _load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key, value)


def main() -> int:
    _load_dotenv(ROOT / ".env")

    os.environ.setdefault("FLASK_DEBUG", "false")
    os.environ.setdefault("SECRET_KEY", "local-smoke-test")
    os.environ.setdefault("LLM_API_KEY", "local-smoke-test")
    os.environ.setdefault("ZEP_API_KEY", "local-smoke-test")
    os.environ.setdefault("UPLOAD_FOLDER", str(BACKEND_DIR / ".tmp" / "uploads"))
    os.environ.setdefault("LOG_DIR", str(BACKEND_DIR / ".tmp" / "logs"))
    os.environ.setdefault("TASKS_DIR", str(BACKEND_DIR / ".tmp" / "uploads" / "tasks"))

    sys.path.insert(0, str(BACKEND_DIR))

    from app import create_app

    app = create_app()
    client = app.test_client()
    response = client.get("/health")

    if response.status_code != 200:
        print(f"/health failed with status {response.status_code}", file=sys.stderr)
        return 1

    print("Backend Railway smoke test passed.")
    print(response.get_json())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
