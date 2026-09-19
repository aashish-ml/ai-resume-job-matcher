from typing import Dict, Any

from src.preprocessing.cleaner import clean_text
from src.preprocessing.section_detector import detect_sections
from src.utils.logger import logger


class PreprocessingPipelineError(Exception):
    """Raised when resume preprocessing fails."""


def preprocess_resume(text: str) -> Dict[str, Any]:
    """
    Complete resume preprocessing pipeline.

    Pipeline:
        Raw Text
            ↓
        Text Cleaning
            ↓
        Section Detection
            ↓
        Structured Resume Data

    Parameters
    ----------
    text : str
        Raw extracted resume text.

    Returns
    -------
    Dict[str, Any]
        Structured preprocessing result.
    """

    if not isinstance(text, str):
        raise PreprocessingPipelineError(
            "Resume text must be a string."
        )

    if not text.strip():
        raise PreprocessingPipelineError(
            "Resume text is empty."
        )

    try:
        logger.info(
            "Starting resume preprocessing pipeline"
        )

        # ---------------------------------------------------------
        # Step 1: Clean raw text
        # ---------------------------------------------------------
        cleaned_text = clean_text(text)

        if not cleaned_text.strip():
            raise PreprocessingPipelineError(
                "Text became empty after cleaning."
            )

        # ---------------------------------------------------------
        # Step 2: Detect resume sections
        # ---------------------------------------------------------
        sections = detect_sections(cleaned_text)

        # ---------------------------------------------------------
        # Step 3: Build structured result
        # ---------------------------------------------------------
        result = {
            "raw_text": text,
            "cleaned_text": cleaned_text,
            "sections": sections,
            "section_count": len(sections),
        }

        logger.info(
            "Resume preprocessing pipeline completed: %d sections",
            len(sections),
        )

        return result

    except PreprocessingPipelineError:
        raise

    except Exception as exc:
        logger.exception(
            "Resume preprocessing pipeline failed"
        )

        raise PreprocessingPipelineError(
            f"Failed to preprocess resume: {exc}"
        ) from exc