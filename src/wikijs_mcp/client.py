"""Small Wiki.js GraphQL client used by the MCP server."""

from __future__ import annotations

import json
import os
from typing import Any
from urllib.parse import urlsplit, urlunsplit

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

    @property
    def upload_url(self) -> str:
        parts = urlsplit(self.url)
        return urlunsplit((parts.scheme, parts.netloc, "/u", "", ""))

    def headers(self) -> dict[str, str]:
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def graphql(
        self,
        query: str,
        variables: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        try:
            response = httpx.post(
                self.url,
                json={"query": query, "variables": variables or {}},
                headers=self.headers(),
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

    def upload_asset(
        self,
        filename: str,
        content: bytes,
        mime_type: str,
        folder_id: int = 0,
    ) -> str:
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        files = [
            (
                "mediaUpload",
                (None, json.dumps({"folderId": folder_id}), "application/json"),
            ),
            ("mediaUpload", (filename, content, mime_type)),
        ]

        try:
            response = httpx.post(
                self.upload_url,
                headers=headers,
                files=files,
                timeout=self.timeout,
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise WikiJSError(f"Wiki.js asset upload failed: {exc}") from exc

        return response.text.strip()


def parse_tags(tags: str | list[str] | None) -> list[str]:
    if tags is None:
        return []
    if isinstance(tags, list):
        return [tag.strip() for tag in tags if tag.strip()]
    return [tag.strip() for tag in tags.split(",") if tag.strip()]
