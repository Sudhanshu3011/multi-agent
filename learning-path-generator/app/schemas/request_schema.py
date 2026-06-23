from typing import List, Optional, Annotated, Literal
from pydantic import BaseModel, Field


class GeneratePathRequest(BaseModel):
    goal: Annotated[
        str,
        Field(
            description="The user's learning objective",
            examples=["Become a Python backend engineer"],
        ),
    ]

    level: Annotated[
        Literal["beginner", "intermediate", "advanced"],
        Field(description="Current experience level"),
    ] = "beginner"

    duration_weeks: Annotated[
        int, Field(ge=1, le=52, description="Length of the learning plan in weeks")
    ] = 8
