from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from app.tools.pdf_extractor import extract_text
from app.graph.builder import run_analysis
from app.core.logger import get_logger
from app.validator.pdf_validator import validate_pdf

router = APIRouter()
logger = get_logger(__name__)


@router.get("/health", summary="Health check")
async def health_check():
    return {"status": "ok", "service": "resume-analyser"}


@router.post("/analyse", summary="Analyse a resume PDF")
async def analyse_resume(
    resume: UploadFile = File(..., description="PDF resume file"),
    job_description: str = Form(
        ...,
        min_length=100,
        max_length=10000,
        description="Paste the complete job description.",
    ),
):
    """
    Upload a PDF resume and return final aggregated result from the graph.
    """

    pdf_bytes = await resume.read()

    validate_pdf(resume, pdf_bytes)

    logger.info(
        f"Received resume: {resume.filename} "
        f"({len(pdf_bytes) / (1024 * 1024):.2f} MB)"
    )

    try:
        extracted_text = extract_text(pdf_bytes)

        final_state = run_analysis(
            extracted_text=extracted_text,
            job_description=job_description.strip(),
        )

        if "final_response" not in final_state:
            raise HTTPException(
                status_code=500,
                detail="Missing final response from pipeline",
            )

        return {"success": True, "data": final_state["final_response"]}

    except Exception:
        logger.exception("Resume analysis pipeline failed")

        raise HTTPException(
            status_code=500,
            detail="Resume analysis failed. Please try again later.",
        )
