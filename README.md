# omniedge

The official Python library for the OmniEdge API

## Quick start

Install:

```bash
pip install omniedge
```

Or from source:

```bash
pip install -e .
```

### Configure Claude Code with OmniEdge

1. Get an OmniEdge API key and (optionally) set:

   ```bash
   export OMNIEDGE_API_KEY="your_api_key"
   export OMNIEDGE_BASE_URL="https://api.omniedge.ai"
   ```

2. Run the setup command and follow the prompts:

   ```bash
   omniedge set claude-code
   ```

   This updates `~/.claude/settings.json` and keeps a backup under `~/.omniedge/backup/claude-code/`.

3. To restore the previous config:

   ```bash
   omniedge reset claude-code
   ```

For advanced usage and development details, see `docs/cli-dev-guide.md`.
