import os
from pathlib import Path

import pytest

from tools.document import binary_document_to_markdown, document_path_to_markdown


class TestBinaryDocumentToMarkdown:
    # Define fixture paths
    FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
    DOCX_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.docx")
    PDF_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.pdf")

    def test_fixture_files_exist(self):
        """Verify test fixtures exist."""
        assert os.path.exists(self.DOCX_FIXTURE), (
            f"DOCX fixture not found at {self.DOCX_FIXTURE}"
        )
        assert os.path.exists(self.PDF_FIXTURE), (
            f"PDF fixture not found at {self.PDF_FIXTURE}"
        )

    def test_binary_document_to_markdown_with_docx(self):
        """Test converting a DOCX document to markdown."""
        # Read binary content from the fixture
        with open(self.DOCX_FIXTURE, "rb") as f:
            docx_data = f.read()

        # Call function
        result = binary_document_to_markdown(docx_data, "docx")

        # Basic assertions to check the conversion was successful
        assert isinstance(result, str)
        assert len(result) > 0
        # Check for typical markdown formatting - this will depend on your actual test file
        assert "#" in result or "-" in result or "*" in result

    def test_binary_document_to_markdown_with_pdf(self):
        """Test converting a PDF document to markdown."""
        # Read binary content from the fixture
        with open(self.PDF_FIXTURE, "rb") as f:
            pdf_data = f.read()

        # Call function
        result = binary_document_to_markdown(pdf_data, "pdf")

        # Basic assertions to check the conversion was successful
        assert isinstance(result, str)
        assert len(result) > 0
        # Check for typical markdown formatting - this will depend on your actual test file
        assert "#" in result or "-" in result or "*" in result


class TestDocumentPathToMarkdown:
    FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
    DOCX_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.docx")
    PDF_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.pdf")

    def test_converts_pdf_from_path(self) -> None:
        result = document_path_to_markdown(self.PDF_FIXTURE)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_converts_docx_from_path(self) -> None:
        result = document_path_to_markdown(self.DOCX_FIXTURE)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_accepts_pathlib_path(self) -> None:
        result = document_path_to_markdown(Path(self.PDF_FIXTURE))
        assert isinstance(result, str)
        assert len(result) > 0

    def test_accepts_relative_path(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.chdir(self.FIXTURES_DIR)
        result = document_path_to_markdown("mcp_docs.pdf")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_uppercase_extension(self, tmp_path: Path) -> None:
        copy = tmp_path / "MCP_DOCS.PDF"
        copy.write_bytes(Path(self.PDF_FIXTURE).read_bytes())
        result = document_path_to_markdown(str(copy))
        assert isinstance(result, str)
        assert len(result) > 0

    def test_matches_binary_converter(self) -> None:
        """The path-based tool should be a thin wrapper over the binary one."""
        with open(self.PDF_FIXTURE, "rb") as f:
            expected = binary_document_to_markdown(f.read(), "pdf")
        assert document_path_to_markdown(self.PDF_FIXTURE) == expected

    def test_nonexistent_path_raises(self, tmp_path: Path) -> None:
        missing = tmp_path / "does_not_exist.pdf"
        with pytest.raises(FileNotFoundError):
            document_path_to_markdown(str(missing))

    def test_directory_path_raises(self, tmp_path: Path) -> None:
        with pytest.raises((IsADirectoryError, PermissionError, OSError)):
            document_path_to_markdown(str(tmp_path))

    def test_unsupported_extension_raises(self, tmp_path: Path) -> None:
        bogus = tmp_path / "notes.xyz"
        bogus.write_bytes(b"hello")
        with pytest.raises(Exception):
            document_path_to_markdown(str(bogus))

    def test_no_extension_raises(self, tmp_path: Path) -> None:
        bogus = tmp_path / "noext"
        bogus.write_bytes(Path(self.PDF_FIXTURE).read_bytes())
        with pytest.raises(Exception):
            document_path_to_markdown(str(bogus))
