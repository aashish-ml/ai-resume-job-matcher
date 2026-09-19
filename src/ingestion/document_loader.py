from pathlib import Path

from src.ingestion.pdf_parser import extract_text_from_pdf
from src.ingestion.docx_parser import extract_text_from_docx
from src.ingestion.text_parser import extract_text_from_txt
from src.utils.logger import logger


class DocumentLoaderError(Exception):
    """Raised when a document cannot be loaded."""


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
}


def load_document(file_path: str | Path) -> str:
    """
    Automatically detect the document type and extract its text.

    Supported formats:
    - PDF
    - DOCX
    - TXT

    Parameters
    ----------
    file_path : str | Path
        Path to the document.

    Returns
    -------
    str
        Extracted document text.

    Raises
    ------
    FileNotFoundError
        If the document does not exist.

    DocumentLoaderError
        If the file type is unsupported.
    """

    path = Path(file_path)

    # ---------------------------------------------------------
    # Validate path
    # ---------------------------------------------------------

    if not path.exists():
        raise FileNotFoundError(
            f"Document not found: {path}"
        )

    if not path.is_file():
        raise DocumentLoaderError(
            f"Provided path is not a file: {path}"
        )

    # ---------------------------------------------------------
    # Detect extension
    # ---------------------------------------------------------

    extension = path.suffix.lower()

    logger.info(
        "Document loader received: %s",
        path.name,
    )

    if extension not in SUPPORTED_EXTENSIONS:
        raise DocumentLoaderError(
            f"Unsupported document type: {extension}. "
            f"Supported types: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )

    # ---------------------------------------------------------
    # Route to appropriate parser
    # ---------------------------------------------------------

    try:

        if extension == ".pdf":

            logger.info(
                "Routing %s to PDF parser",
                path.name,
            )

            return extract_text_from_pdf(path)

        if extension == ".docx":

            logger.info(
                "Routing %s to DOCX parser",
                path.name,
            )

            return extract_text_from_docx(path)

        if extension == ".txt":

            logger.info(
                "Routing %s to TXT parser",
                path.name,
            )

            return extract_text_from_txt(path)

    except Exception as exc:

        logger.exception(
            "Document loading failed for %s",
            path.name,
        )

        raise DocumentLoaderError(
            f"Failed to load document '{path.name}': {exc}"
        ) from exc

    raise DocumentLoaderError(
        f"No parser available for extension: {extension}"
    )