# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Setup
uv venv
source .venv/bin/activate         # PowerShell: .venv\Scripts\Activate.ps1
uv pip install -e .

# Run the MCP server
uv run main.py

# Tests
uv run pytest
uv run pytest tests/test_document.py::TestBinaryDocumentToMarkdown::test_binary_document_to_markdown_with_pdf
```

## Architecture

This is an MCP (Model Context Protocol) server exposing document-processing tools to AI assistants.

- `main.py` — entry point. Instantiates `FastMCP("docs")`, registers tool functions via `mcp.tool()(fn)`, then calls `mcp.run()`. New tools are wired up here.
- `tools/` — each module holds plain Python functions (no MCP coupling). Functions are registered into the server from `main.py`. This keeps tools unit-testable without spinning up the server (see `tests/test_document.py` calling `binary_document_to_markdown` directly).
- `tests/fixtures/` — binary documents (`mcp_docs.docx`, `mcp_docs.pdf`) used by document conversion tests.

Document conversion goes through `markitdown` (`MarkItDown().convert(BytesIO(...), StreamInfo(extension=file_type))`), so any new format supported by markitdown can be wired in by extension string.

## Defining MCP tools (from README)

Tools are plain Python functions registered with `mcp.tool()(fn)` in `main.py`. Their docstrings and parameter descriptions are what the LLM sees, so write them carefully.

**Docstring structure:**
- One-line summary first
- Detailed explanation of functionality
- "When to use" (and when not to use) the tool
- Usage examples with expected input/output

**Parameters:** use `pydantic.Field(description=...)` for every parameter so the description reaches the MCP schema:

```python
from pydantic import Field

def my_tool(
    param1: str = Field(description="Detailed description of this parameter"),
    param2: int = Field(description="Explain what this parameter does"),
) -> ReturnType:
    """Comprehensive docstring here."""
    ...
```

`tools/math.py::add` is the canonical example — follow that shape for new tools.
