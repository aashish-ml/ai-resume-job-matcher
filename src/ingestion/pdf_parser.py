from pathlib import Path

from pypdf import PdfReader

from src.utils.logger import logger
from src.utils.validators import (
    FileValidationError,
    validate_uploaded_file,
)


class PDFExtractionError(Exception):
    """Raised when PDF text extraction fails."""


def extract_text_from_pdf(file_path: str | Path) -> str:
    """
    Extract text from a PDF resume.

    Parameters
    ----------
    file_path : str | Path
        Path to the PDF document.

    Returns
    -------
    str
        Extracted text from all readable pages.

    Raises
    ------
    FileNotFoundError
        If the PDF does not exist.

    FileValidationError
        If the file extension or size is invalid.

    PDFExtractionError
        If PDF reading or text extraction fails.
    """

    path = Path(file_path)

    # ---------------------------------------------------------
    # File existence
    # ---------------------------------------------------------

    if not path.exists():
        raise FileNotFoundError(
            f"PDF file not found: {path}"
        )

    if not path.is_file():
        raise FileValidationError(
            "Provided PDF path is not a file."
        )

    # ---------------------------------------------------------
    # File validation
    # ---------------------------------------------------------

    file_size = path.stat().st_size

    extension = validate_uploaded_file(
        filename=path.name,
        file_size=file_size,
    )

    if extension != ".pdf":
        raise FileValidationError(
            "PDF parser can only process .pdf files."
        )

    logger.info(
        "Starting PDF text extraction: %s",
        path.name,
    )

    # ---------------------------------------------------------
    # PDF extraction
    # ---------------------------------------------------------

    try:
        reader = PdfReader(str(path))

        if not reader.pages:
            raise PDFExtractionError(
                "PDF contains no pages."
            )

        extracted_pages: list[str] = []

        for page_number, page in enumerate(
            reader.pages,
            start=1,
        ):
            try:
                text = page.extract_text() or ""

                text = text.strip()

                if text:
                    extracted_pages.append(text)

                logger.debug(
                    "Processed PDF page %d: %d characters",
                    page_number,
                    len(text),
                )

            except Exception as exc:
                logger.warning(
                    "Could not extract text from PDF page %d: %s",
                    page_number,
                    exc,
                )

        # -----------------------------------------------------
        # Combine pages
        # -----------------------------------------------------

        extracted_text = "\n\n".join(
            extracted_pages
        ).strip()

        if not extracted_text:
            raise PDFExtractionError(
                "No readable text was extracted from the PDF. "
                "The document may be scanned/image-based and "
                "may require OCR."
            )

        logger.info(
            "PDF extraction completed: %s (%d characters)",
            path.name,
            len(extracted_text),
        )

        return extracted_text

    except PDFExtractionError:
        raise

    except Exception as exc:
        logger.exception(
            "PDF extraction failed for %s",
            path.name,
        )

        raise PDFExtractionError(
            f"Failed to extract text from PDF: {exc}"
        ) from exc