# Wiki.js MCP Writer Skill Notes

This note records the local Codex skill pattern used for writing Wiki.js pages
through the Wiki.js MCP Server.

## Purpose

The skill helps Codex consistently create and update Wiki.js documents through a
configured MCP server.

It is useful for:

- Creating project notes in Wiki.js.
- Adding date and time to page titles.
- Uploading images through `wikijs_upload_asset`.
- Embedding uploaded images in Wiki.js pages.
- Verifying created pages after write operations.

## Recommended Location

Local Codex skills should live outside this repository:

```text
~/.codex/skills/wikijs-mcp-writer/SKILL.md
```

Keeping the skill local is usually better when it contains personal workflow
preferences, local paths, or private Wiki.js conventions.

## Minimal Skill Structure

```markdown
---
name: wikijs-mcp-writer
description: Use when writing, updating, or publishing Wiki.js pages through a configured Wiki.js MCP server, especially when creating project notes, timestamped documents, or pages containing uploaded images/assets.
---

# Wiki.js MCP Writer

## Workflow

When asked to create a Wiki.js document:

1. Use the configured Wiki.js MCP server.
2. Put date and time in the title when the user asks for a timestamped document.
3. Prefer paths under `/projects/...` for project documentation unless the user specifies another location.
4. Create Markdown content with clear headings and concise Korean text when the user is Korean.
5. After creating a page, verify it with `wikijs_list_pages` or `wikijs_get_page_by_id`.
```

## Image Handling

For this Wiki.js setup, Markdown image syntax may not render reliably. Prefer an
HTML image tag after uploading an image:

```html
<img src="/uploaded-file.png" alt="description" width="600">
```

Markdown syntax can still be returned as a convenience, but it should not be the
only representation used in pages where visual confirmation matters:

```markdown
![description](/uploaded-file.png)
```

## Asset Naming

When uploading images, use explicit filenames. Prefer this pattern:

```text
project-or-page-purpose-YYYYMMDD-HHMMSS.ext
```

Examples:

- `wikijs-mcp-upload-test-20260410-144438.png`
- `anilife-character-dice-20260410-145200.png`

Avoid generic names such as `image.png`, `test.png`, or `upload.png` unless the
user explicitly asks.

## Validation

After writing a page with an image:

1. Fetch the page with `wikijs_get_page_by_id`.
2. Confirm the page content contains the expected image URL.
3. Confirm the page content contains an `<img>` tag when visual rendering matters.
4. Use a real image for visual testing. A 1x1 PNG can upload successfully but may
   look invisible on the rendered page.

## Git Decision

Do not commit local skills automatically.

Consider committing this note or an example skill only if:

- It contains no private IPs, tokens, or private Wiki.js paths.
- It documents a reusable public workflow.
- It helps future users of this repository operate the MCP server.

Keep the actual local skill private if it includes personal conventions or local
folder mappings.
