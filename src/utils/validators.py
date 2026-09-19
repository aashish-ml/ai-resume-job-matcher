from pathlib import Path


# ---------------------------------------------------------
# Supported Resume File Types
# ---------------------------------------------------------

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
}


# ---------------------------------------------------------
# Maximum File Size
# ---------------------------------------------------------

MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024


# ---------------------------------------------------------
# Custom Validation Error
# ---------------------------------------------------------

class FileValidationError(ValueError):
    """Raised when an uploaded file fails validation."""


# ---------------------------------------------------------
# Extension Validation
# ---------------------------------------------------------

def validate_file_extension(filename: str) -> str:
    """
    Validate and return a normalized file extension.

    Parameters
    ----------
    filename : str
        Name of the uploaded file.

    Returns
    -------
    str
        Lowercase file extension.

    Raises
    ------
    FileValidationError
        If the filename is invalid or unsupported.
    """

    if not filename or not filename.strip():
        raise FileValidationError("Filename cannot be empty.")

    extension = Path(filename).suffix.lower()

    if not extension:
        raise FileValidationError(
            "File must have an extension."
        )

    if extension not in ALLOWED_EXTENSIONS:
        allowed = ", ".join(sorted(ALLOWED_EXTENSIONS))

        raise FileValidationError(
            f"Unsupported file type '{extension}'. "
            f"Allowed types: {allowed}"
        )

    return extension


# ---------------------------------------------------------
# File Size Validation
# ---------------------------------------------------------

def validate_file_size(file_size: int) -> None:
    """
    Validate uploaded file size.

    Parameters
    ----------
    file_size : int
        File size in bytes.

    Raises
    ------
    FileValidationError
        If the file is empty or exceeds the configured limit.
    """

    if file_size <= 0:
        raise FileValidationError(
            "Uploaded file is empty."
        )

    if file_size > MAX_FILE_SIZE_BYTES:
        raise FileValidationError(
            f"File is too large. Maximum allowed size is "
            f"{MAX_FILE_SIZE_MB} MB."
        )


# ---------------------------------------------------------
# Filename Validation
# ---------------------------------------------------------

def validate_filename(filename: str) -> str:
    """
    Perform basic filename validation.

    Returns the original filename when valid.
    """

    if not filename or not filename.strip():
        raise FileValidationError(
            "Filename cannot be empty."
        )

    filename = filename.strip()

    if len(filename) > 255:
        raise FileValidationError(
            "Filename is too long."
        )

    # Prevent directory traversal through uploaded filenames.
    if Path(filename).name != filename:
        raise FileValidationError(
            "Invalid filename."
        )

    return filename


# ---------------------------------------------------------
# Complete File Validation
# ---------------------------------------------------------

def validate_uploaded_file(
    filename: str,
    file_size: int,
) -> str:
    """
    Run all basic validation checks for an uploaded file.

    Returns
    -------
    str
        Validated file extension.
    """

    validate_filename(filename)

    extension = validate_file_extension(filename)

    validate_file_size(file_size)

    return extension