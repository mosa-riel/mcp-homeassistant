"""Entrypoint for the Home Assistant MCP add-on.

Wraps upstream `ha-mcp` (homeassistant-ai/ha-mcp). Credentials, in priority order:
  1. add-on options `ha_url` / `ha_token`  (pasted long-lived token — fallback path)
  2. SUPERVISOR_TOKEN + the Supervisor core proxy  (default; needs homeassistant_api:true)
Then runs ha-mcp in streamable-HTTP mode (`ha-mcp-web`) so the agent connects by url.
"""

from __future__ import annotations

import json
import os


def _options() -> dict:
    try:
        with open("/data/options.json") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def main() -> None:
    opts = _options()

    # URL: explicit option > env > Supervisor core proxy (http://supervisor/core → /api).
    url = (opts.get("ha_url") or os.getenv("HOMEASSISTANT_URL") or "http://supervisor/core").rstrip("/")

    # Token: pasted option > explicit env > Supervisor-injected token.
    token = opts.get("ha_token") or os.getenv("HOMEASSISTANT_TOKEN") or os.getenv("SUPERVISOR_TOKEN", "")

    os.environ["HOMEASSISTANT_URL"] = url
    os.environ["HOMEASSISTANT_TOKEN"] = token
    os.environ.setdefault("MCP_HOST", "0.0.0.0")
    os.environ.setdefault("MCP_PORT", str(opts.get("mcp_port") or 8086))

    if not token:
        raise SystemExit(
            "No Home Assistant token: set homeassistant_api:true (SUPERVISOR_TOKEN) "
            "or paste a long-lived token in the add-on's ha_token option."
        )

    from ha_mcp.__main__ import main_web

    main_web()


if __name__ == "__main__":
    main()
