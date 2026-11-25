"""Tiny OpenAI-compatible client: one POST /chat/completions, no SDK dependency."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

BASE = os.environ.get("LLM_BASE_URL", "http://localhost:8000/v1").rstrip("/")
KEY = os.environ.get("LLM_API_KEY", "sk-local")
MODEL = os.environ.get("LLM_MODEL", "my-model")


def chat(prompt: str, system: str | None = None, timeout: int = 60) -> str:
    """Send one prompt, return the assistant text. Raises on HTTP errors."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    body = json.dumps({"model": MODEL, "messages": messages, "temperature": 0}).encode()
    req = urllib.request.Request(
        f"{BASE}/chat/completions",
        data=body,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {KEY}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as err:
        raise RuntimeError(f"endpoint returned {err.code}: {err.read()[:200]!r}") from err
    return data["choices"][0]["message"]["content"]
