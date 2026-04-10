# Wiki.js MCP Server

FastMCP HTTP server that exposes Wiki.js GraphQL operations as MCP tools.

## Setup

```bash
source .venv/bin/activate
pip install -e .
cp .env.example .env
```

Put your Wiki.js API token in `.env`:

```bash
WIKIJS_API_TOKEN=...
```

## Run

This project uses FastMCP's HTTP transport, not stdio.

```bash
source .venv/bin/activate
python -m wikijs_mcp.server
```

Default endpoint:

```text
http://127.0.0.1:8000/mcp
```

Override server settings with environment variables:

```bash
MCP_HOST=0.0.0.0 MCP_PORT=8787 MCP_PATH=/mcp python -m wikijs_mcp.server
```

## Docker

Docker Hub image:

```text
https://hub.docker.com/r/disturb8264/wikijs-mcp-server
```

Pull the published image:

```bash
docker pull disturb8264/wikijs-mcp-server:latest
```

Build from the repository root:

```bash
docker build -f docker/Dockerfile -t wikijs-mcp-server .
```

Run with your local `.env`:

```bash
docker run --rm \
  --name wikijs-mcp-server \
  -p 8000:8000 \
  --env-file .env \
  disturb8264/wikijs-mcp-server:latest
```

Run with Docker Compose:

```bash
docker compose up -d --build
```

If host port `8000` is already in use:

```bash
MCP_HTTP_PORT=18000 docker compose up -d --build
```

## Tools

- `wikijs_health`: Check Wiki.js connectivity.
- `wikijs_graphql`: Run a raw GraphQL query against Wiki.js.
- `wikijs_list_pages`: List Wiki.js pages.
- `wikijs_get_page_by_id`: Fetch one page by numeric page id.
- `wikijs_create_page`: Create a Markdown page.
- `wikijs_update_page`: Update page fields by id.
- `wikijs_move_page`: Move a page to a new path.

Create, update, and move operations modify the real Wiki.js instance.
