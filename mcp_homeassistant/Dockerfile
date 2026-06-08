# Thin wrapper over the upstream multi-arch ha-mcp image. We can't set the container
# CMD from a HA add-on manifest, so we build FROM upstream and override the entrypoint
# with run.py (maps the Supervisor token → HOMEASSISTANT_TOKEN, then runs ha-mcp-web).
FROM ghcr.io/homeassistant-ai/ha-mcp:latest

ENV PYTHONUNBUFFERED=1 \
    MCP_HOST=0.0.0.0 \
    MCP_PORT=8086

COPY run.py /run.py

EXPOSE 8086
ENTRYPOINT []
CMD ["python", "/run.py"]
