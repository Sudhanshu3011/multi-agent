import logging

from fastapi import APIRouter, HTTPException

from app.graph.builder import graph_app

from app.schemas.request_schema import GeneratePathRequest
from app.schemas.planner_schema import LearningSchedule

router = APIRouter()

logger = logging.getLogger("app.api")


@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "learning-path-agent",
    }


@router.post("/generate-path", response_model=LearningSchedule)
async def generate_path(
    request: GeneratePathRequest,
):

    inputs = {
        "goal": request.goal,
        "level": request.level,
        "duration_weeks": request.duration_weeks,
    }

    try:
        result = await graph_app.ainvoke(inputs)

        learning_schedule = result.get("learning_schedule")

        if learning_schedule is None:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate learning schedule",
            )

        return learning_schedule

    except Exception as exc:

        logger.exception("Error generating learning schedule")

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )
