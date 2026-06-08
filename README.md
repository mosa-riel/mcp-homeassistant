# mcp-homeassistant

Home Assistant control MCP for the [reSpeaker agent](https://gitlab.zzapps.nl/development/respeaker-agent),
wrapping upstream [`ha-mcp`](https://github.com/homeassistant-ai/ha-mcp) in
streamable-HTTP mode (`ha-mcp-web`). The agent connects by `url`.

## Credentials (priority order)

1. Add-on options `ha_url` + `ha_token` — a pasted long-lived token (fallback).
2. **`SUPERVISOR_TOKEN`** + the Supervisor core proxy (`http://supervisor/core`) —
   default, enabled by `homeassistant_api: true`. No token to create or manage; HA's
   role-scoping (`hassio_role`) bounds what it can do.

`run.py` resolves these and launches `ha-mcp-web`.

## Home Assistant add-on

Bridged network; agent reaches it at `http://local-mcp_homeassistant:8086/mcp`. Copy
this folder into the HA host's `/addons` dir → Install. Leave both options blank to use
the Supervisor token; paste a token only if the proxy path doesn't work for your setup.

## Verify (on the HA host)

After install, check the add-on log shows `ha-mcp-web` serving on `:8086`, then from the
agent confirm the `home-assistant` MCP shows `connected: true` with its tools.
