# Docker

Build the image from the repository root:

```bash
docker build -f docker/Dockerfile -t wikijs-mcp-server .
```

Run with environment variables:

```bash
docker run --rm \
  --name wikijs-mcp-server \
  -p 8000:8000 \
  -e WIKIJS_URL=https://wiki.example.com/graphql \
  -e WIKIJS_API_TOKEN=replace-me \
  -e WIKIJS_LOCALE=ko \
  wikijs-mcp-server
```

Or run with a local `.env` file:

```bash
docker run --rm \
  --name wikijs-mcp-server \
  -p 8000:8000 \
  --env-file .env \
  wikijs-mcp-server
```

Default MCP endpoint:

```text
http://127.0.0.1:8000/mcp
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Uploaded Wiki.js assets are sent through the Wiki.js `/u` endpoint. The MCP
upload tool accepts base64 file content and returns asset metadata, a URL, and
a Markdown image/link snippet.

## Docker Compose

From the repository root:

```bash
docker compose up -d --build
```

If host port `8000` is already in use:

```bash
MCP_HTTP_PORT=18000 docker compose up -d --build
```

Stop:

```bash
docker compose down
```
