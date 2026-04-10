"""Small Wiki.js GraphQL client used by the MCP server."""

from __future__ import annotations

import os
from typing import Any

import httpx


class WikiJSError(RuntimeError):
    """Raised when Wiki.js returns a transport or GraphQL error."""


class WikiJSClient:
    def __init__(
        self,
        url: str | None = None,
        token: str | None = None,
        timeout: float = 10.0,
    ) -> None:
        self.url = url or os.getenv("WIKIJS_URL")
        if not self.url:
            raise WikiJSError("WIKIJS_URL must be set to the Wiki.js GraphQL endpoint.")
        self.token = token if token is not None else os.getenv("WIKIJS_API_TOKEN")
        self.timeout = timeout

    def graphql(
        self,
        query: str,
        variables: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        try:
            response = httpx.post(
                self.url,
                json={"query": query, "variables": variables or {}},
                headers=headers,
                timeout=self.timeout,
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise WikiJSError(f"Wiki.js request failed: {exc}") from exc

        try:
            payload = response.json()
        except ValueError as exc:
            raise WikiJSError(f"Wiki.js returned non-JSON response: {response.text[:500]}") from exc

        if payload.get("errors"):
            raise WikiJSError(f"Wiki.js GraphQL errors: {payload['errors']}")

        return payload


def parse_tags(tags: str | list[str] | None) -> list[str]:
    if tags is None:
        return []
    if isinstance(tags, list):
        return [tag.strip() for tag in tags if tag.strip()]
    return [tag.strip() for tag in tags.split(",") if tag.strip()]
