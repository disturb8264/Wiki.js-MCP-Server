"""FastMCP HTTP server exposing Wiki.js GraphQL operations."""

from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from wikijs_mcp.client import WikiJSClient, parse_tags


DEFAULT_QUERY = """
{
  pages {
    list {
      id
      path
      title
    }
  }
}
""".strip()

GET_PAGE_BY_ID_QUERY = """
query GetPageById($id: Int!) {
  pages {
    single(id: $id) {
      id
      path
      title
      description
      content
      createdAt
      updatedAt
    }
  }
}
""".strip()

CREATE_PAGE_MUTATION = """
mutation CreatePage(
  $content: String!
  $description: String!
  $editor: String!
  $isPublished: Boolean!
  $isPrivate: Boolean!
  $locale: String!
  $path: String!
  $tags: [String]!
  $title: String!
) {
  pages {
    create(
      content: $content
      description: $description
      editor: $editor
      isPublished: $isPublished
      isPrivate: $isPrivate
      locale: $locale
      path: $path
      tags: $tags
      title: $title
    ) {
      responseResult {
        succeeded
        errorCode
        slug
        message
      }
      page {
        id
        path
        title
      }
    }
  }
}
""".strip()

UPDATE_PAGE_MUTATION = """
mutation UpdatePage(
  $id: Int!
  $content: String
  $description: String
  $editor: String
  $isPublished: Boolean
  $isPrivate: Boolean
  $locale: String
  $path: String
  $tags: [String]
  $title: String
) {
  pages {
    update(
      id: $id
      content: $content
      description: $description
      editor: $editor
      isPublished: $isPublished
      isPrivate: $isPrivate
      locale: $locale
      path: $path
      tags: $tags
      title: $title
    ) {
      responseResult {
        succeeded
        errorCode
        slug
        message
      }
      page {
        id
        path
        title
      }
    }
  }
}
""".strip()

MOVE_PAGE_MUTATION = """
mutation MovePage(
  $id: Int!
  $destinationPath: String!
  $destinationLocale: String!
) {
  pages {
    move(
      id: $id
      destinationPath: $destinationPath
      destinationLocale: $destinationLocale
    ) {
      responseResult {
        succeeded
        errorCode
        slug
        message
      }
    }
  }
}
""".strip()


load_dotenv()

mcp = FastMCP(
    name="wikijs-mcp",
    instructions="Use these tools to read and manage pages in a configured Wiki.js instance.",
)


def wikijs() -> WikiJSClient:
    return WikiJSClient()


@mcp.custom_route("/health", methods=["GET"], include_in_schema=False)
async def health_check(request: Request) -> Response:
    return JSONResponse({"status": "ok", "service": "wikijs-mcp"})


@mcp.tool
def wikijs_health() -> dict[str, Any]:
    """Check connectivity to the configured Wiki.js GraphQL API."""
    client = wikijs()
    result = client.graphql(DEFAULT_QUERY)
    pages = result["data"]["pages"]["list"]
    return {
        "ok": True,
        "url": client.url,
        "page_count": len(pages),
    }


@mcp.tool
def wikijs_graphql(query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
    """Run a raw GraphQL query or mutation against Wiki.js."""
    return wikijs().graphql(query, variables)


@mcp.tool
def wikijs_list_pages() -> list[dict[str, Any]]:
    """List Wiki.js pages with id, path, and title."""
    result = wikijs().graphql(DEFAULT_QUERY)
    return result["data"]["pages"]["list"]


@mcp.tool
def wikijs_get_page_by_id(page_id: int) -> dict[str, Any] | None:
    """Fetch a Wiki.js page by numeric page id."""
    result = wikijs().graphql(GET_PAGE_BY_ID_QUERY, {"id": page_id})
    return result["data"]["pages"]["single"]


@mcp.tool
def wikijs_create_page(
    path: str,
    title: str,
    content: str,
    description: str = "",
    tags: str | list[str] | None = None,
    editor: str = "markdown",
    locale: str | None = None,
    is_published: bool = True,
    is_private: bool = False,
) -> dict[str, Any]:
    """Create a Markdown page in Wiki.js."""
    variables = {
        "content": content,
        "description": description,
        "editor": editor,
        "isPublished": is_published,
        "isPrivate": is_private,
        "locale": locale or os.getenv("WIKIJS_LOCALE", "ko"),
        "path": path,
        "tags": parse_tags(tags),
        "title": title,
    }
    result = wikijs().graphql(CREATE_PAGE_MUTATION, variables)
    return result["data"]["pages"]["create"]


@mcp.tool
def wikijs_update_page(
    page_id: int,
    path: str | None = None,
    title: str | None = None,
    content: str | None = None,
    description: str | None = None,
    tags: str | list[str] | None = None,
    editor: str | None = None,
    locale: str | None = None,
    is_published: bool | None = None,
    is_private: bool | None = None,
) -> dict[str, Any]:
    """Update Wiki.js page fields by numeric page id."""
    variables: dict[str, Any] = {"id": page_id}
    optional_values = {
        "path": path,
        "title": title,
        "content": content,
        "description": description,
        "editor": editor,
        "locale": locale,
        "isPublished": is_published,
        "isPrivate": is_private,
    }
    variables.update({key: value for key, value in optional_values.items() if value is not None})
    if tags is not None:
        variables["tags"] = parse_tags(tags)

    result = wikijs().graphql(UPDATE_PAGE_MUTATION, variables)
    return result["data"]["pages"]["update"]


@mcp.tool
def wikijs_move_page(
    page_id: int,
    destination_path: str,
    destination_locale: str | None = None,
) -> dict[str, Any]:
    """Move a Wiki.js page to a new path."""
    variables = {
        "id": page_id,
        "destinationPath": destination_path,
        "destinationLocale": destination_locale or os.getenv("WIKIJS_LOCALE", "ko"),
    }
    result = wikijs().graphql(MOVE_PAGE_MUTATION, variables)
    return result["data"]["pages"]["move"]


def main() -> None:
    host = os.getenv("MCP_HOST", "127.0.0.1")
    port = int(os.getenv("MCP_PORT", "8000"))
    path = os.getenv("MCP_PATH", "/mcp")
    mcp.run(transport="http", host=host, port=port, path=path)


if __name__ == "__main__":
    main()
