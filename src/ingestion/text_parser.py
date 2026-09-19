from pathlib import Path

from src.utils.logger import logger
from src.utils.validators import (
    FileValidationError,
    validate_uploaded_file,
)


class TXTExtractionError(Exception):
    """Raised when TXT text extraction fails."""


def extract_text_from_txt(file_path: str | Path) -> str:
    """
    Extract text from a TXT resume.

    Parameters
    ----------
    file_path : str | Path
        Path to the TXT document.

    Returns
    -------
    str
        Extracted and stripped text.

    Raises
    ------
    FileNotFoundError
        If the TXT file does not exist.

    FileValidationError
        If the file is invalid or unsupported.

    TXTExtractionError
        If TXT extraction fails or the file contains no text.
    """

    path = Path(file_path)

    # ---------------------------------------------------------
    # File existence
    # ---------------------------------------------------------

    if not path.exists():
        raise FileNotFoundError(
            f"TXT file not found: {path}"
        )

    if not path.is_file():
        raise FileValidationError(
            "Provided TXT path is not a file."
        )

    # ---------------------------------------------------------
    # File validation
    # ---------------------------------------------------------

    file_size = path.stat().st_size

    extension = validate_uploaded_file(
        filename=path.name,
        file_size=file_size,
    )

    if extension != ".txt":
        raise FileValidationError(
            "TXT parser can only process .txt files."
        )

    logger.info(
        "Starting TXT text extraction: %s",
        path.name,
    )

    # ---------------------------------------------------------
    # Text extraction
    # ---------------------------------------------------------

    try:
        # UTF-8 first, with graceful fallback for common
        # Windows-encoded text files.
        try:
            extracted_text = path.read_text(
                encoding="utf-8"
            )
        except UnicodeDecodeError:
            extracted_text = path.read_text(
                encoding="cp1252"
            )

        extracted_text = extracted_text.strip()

        if not extracted_text:
            raise TXTExtractionError(
                "No readable text was found in the TXT file."
            )

        logger.info(
            "TXT extraction completed: %s (%d characters)",
            path.name,
            len(extracted_text),
        )

        return extracted_text

    except TXTExtractionError:
        raise

    except Exception as exc:
        logger.exception(
            "TXT extraction failed for %s",
            path.name,
        )

        raise TXTExtractionError(
            f"Failed to extract text from TXT: {exc}"
        ) from exc