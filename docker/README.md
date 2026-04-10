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
