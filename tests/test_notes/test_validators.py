from io import BytesIO
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException, UploadFile
from starlette.datastructures import Headers

from app.routes.notes import validate_upload_file

pytestmark = pytest.mark.asyncio


def create_upload_file(
    filename: str,
    content_type: str,
    content: bytes = b"Sample content",
) -> UploadFile:
    """Helper to create UploadFile for testing."""
    return UploadFile(
        file=BytesIO(content),
        filename=filename,
        headers=Headers({"content-type": content_type}),
    )


class TestValidateUploadFile:
    async def test_validate_upload_file_valid_txt(self) -> None:
        file = create_upload_file(
            filename="test.txt", content_type="text/plain", content=b"Sample content"
        )
        result = await validate_upload_file(file)
        assert result == "Sample content"

    async def test_validate_upload_file_invalid_extension(self) -> None:
        file = create_upload_file(
            filename="test.md", content_type="text/markdown", content=b"Sample content"
        )
        with pytest.raises(HTTPException) as exc_info:
            await validate_upload_file(file)
        assert exc_info.value.status_code == 400

    async def test_validate_upload_file_no_filename(self) -> None:
        """Test validation with no filename"""
        file = create_upload_file(
            filename="", content_type="text/plain", content=b"Sample content"
        )
        result = await validate_upload_file(file)
        assert result == "Sample content"

    async def test_validate_upload_file_empty_content(self) -> None:
        file = create_upload_file(
            filename="empty.txt", content_type="text/plain", content=b"   "
        )
        with pytest.raises(HTTPException) as exc_info:
            await validate_upload_file(file)
        assert exc_info.value.status_code == 400

    async def test_validate_upload_file_large_content(self) -> None:
        # Create a mock UploadFile
        mock_file = AsyncMock(spec=UploadFile)
        mock_file.filename = "large.txt"
        mock_file.content_type = "text/plain"

        # Mock read to return large content (11MB)
        mock_content = MagicMock(bytes)
        mock_content.__len__.return_value = 11 * 1024 * 1024  # 11MB
        mock_file.read = AsyncMock(return_value=mock_content)

        with pytest.raises(HTTPException) as exc_info:
            await validate_upload_file(mock_file)
        assert exc_info.value.status_code == 413
        assert "too large" in exc_info.value.detail.lower()
