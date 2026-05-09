from io import BytesIO
from pathlib import Path
from typing import Union

from markitdown import MarkItDown, StreamInfo
from pydantic import Field


def binary_document_to_markdown(binary_data: bytes, file_type: str) -> str:
    """Converts binary document data to markdown-formatted text."""
    md = MarkItDown()
    file_obj = BytesIO(binary_data)
    stream_info = StreamInfo(extension=file_type)
    result = md.convert(file_obj, stream_info=stream_info)
    return result.text_content


def document_path_to_markdown(
    path: Union[str, Path] = Field(
        description="Filesystem path to a PDF or DOCX document to convert."
    ),
) -> str:
    """Read a PDF or DOCX file from disk and return its contents as markdown.

    Reads the file at the given path, detects the format from its extension,
    and converts the contents to markdown-formatted text.

    When to use:
    - When you have a local PDF or DOCX file and need its text as markdown
      for further processing or summarization.

    When not to use:
    - For documents that are not on the local filesystem (use a fetch tool first).
    - For unsupported formats (anything other than .pdf or .docx).

    Examples:
    >>> document_path_to_markdown("report.pdf")
    '# Report\\n...'
    >>> document_path_to_markdown("notes.docx")
    '# Notes\\n...'
    """
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"No such file: {file_path}")
    if file_path.is_dir():
        raise IsADirectoryError(f"Path is a directory, not a file: {file_path}")

    extension = file_path.suffix.lstrip(".").lower()
    if not extension:
        raise ValueError(f"Cannot determine document type — no extension on {file_path}")
    if extension not in {"pdf", "docx"}:
        raise ValueError(f"Unsupported document extension: .{extension}")

    return binary_document_to_markdown(file_path.read_bytes(), extension)
