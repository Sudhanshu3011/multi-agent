from typing import List, Optional
from pydantic import BaseModel, Field
from app.schemas.resource_schema import Resource


class LearningPhase(BaseModel):
    phase: int = Field(..., description="The phase number (1-based)")

    title: str = Field(
        ..., description="Phase title such as Foundations or Core Concepts"
    )

    description: str = Field(
        ...,
        description=("Explain what this phase teaches and what concepts are covered."),
    )

    phase_impact: str = Field(
        ...,
        description=(
            "Explain why this phase is important in the learning journey "
            "and how the suggested resources contribute to achieving the phase objectives."
        ),
    )

    weeks: List[int] = Field(..., description="Week numbers included in this phase")

    topics: List[str] = Field(..., description="Topics covered during this phase")

    estimated_hours: int = Field(
        ..., description="Estimated hours needed for this phase"
    )

    resources: List[Resource] = Field(
        default_factory=list,
        description="Curated resources enriched with descriptions and learning impact",
    )

    learning_objectives: List[str] = Field(
        ..., description="Learning objectives for this phase"
    )

    prerequisites: List[str] = Field(
        default_factory=list, description="Prerequisites for this phase"
    )

    assessment: str = Field(..., description="How to assess progress in this phase")


class LearningSchedule(BaseModel):
    goal: str = Field(..., description="The learning goal")
    level: str = Field(..., description="Target skill level")
    duration_weeks: int = Field(..., description="Total duration in weeks")
    total_estimated_hours: int = Field(..., description="Total estimated hours needed")
    recommended_pace: str = Field(
        ..., description="Recommended daily/weekly pace (e.g., '5 hours/week')"
    )
    phases: List[LearningPhase] = Field(
        ..., description="Learning phases with step-by-step progression"
    )
    progression_flow: str = Field(
        ...,
        description="Detailed description of how to progress through the learning path",
    )
    milestones: List[str] = Field(..., description="Key milestones to track progress")
    tips_for_success: List[str] = Field(
        ..., description="Tips and best practices for successful learning"
    )
