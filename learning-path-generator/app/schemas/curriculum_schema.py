from typing import List, Optional
from pydantic import BaseModel, Field
from app.schemas.resource_schema import Resource


class WeekPlan(BaseModel):
    week: int = Field(..., description="The week index (1-based)")
    topics: List[str] = Field(..., description="Topics covered in this week")
    estimated_hours: int = Field(
        ..., description="Estimated hours needed to study this week's content"
    )
    resources: List[Resource] = Field(
        default_factory=list, description="Recommended resources for this week"
    )


class LearningPlan(BaseModel):
    goal: str = Field(..., description="The parsed and validated learning goal")
    level: str = Field(..., description="Target skill level")
    duration_weeks: int = Field(..., description="Target duration of the path in weeks")
    curriculum: List[WeekPlan] = Field(
        ..., description="Week-by-week curriculum syllabus structure"
    )
