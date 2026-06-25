from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional

from app.graph.builder import run_analysis
from app.core.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)

MAX_FILE_SIZE_MB = 5
ALLOWED_CONTENT_TYPES = {"application/pdf"}


@router.get("/health", summary="Health check")
async def health_check():
    return {"status": "ok", "service": "resume-analyser"}


@router.post("/analyse", summary="Analyse a resume PDF")
async def analyse_resume(
    resume: UploadFile = File(..., description="PDF resume file"),
    job_description: str = Form(
        ...,
        description=(
            "Paste the full job description here. "
            "Include important keywords such as required skills, experience, and technologies. "
            "The more detailed it is, the better the resume analysis results will be."
        ),
    ),
) -> JSONResponse:
    """
    Upload a PDF resume and return final aggregated result from the graph.
    """

    if resume.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type '{resume.content_type}'. Only PDF files are accepted.",
        )

    pdf_bytes = await resume.read()

    size_mb = len(pdf_bytes) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=413,
            detail=f"File too large ({size_mb:.1f} MB). Maximum allowed size is {MAX_FILE_SIZE_MB} MB.",
        )

    logger.info(f"Received resume: {resume.filename} ({size_mb:.2f} MB)")

    try:
        final_state = run_analysis(
            pdf_bytes=pdf_bytes,
            job_description=(job_description.strip()),
        )

    except Exception as exc:
        logger.exception("Resume analysis pipeline failed")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {exc}",
        )

    if final_state.get("error"):
        raise HTTPException(
            status_code=422,
            detail=final_state["error"],
        )

    return JSONResponse(
        status_code=200,
        content=final_state.get("final_response", {}),
    )
