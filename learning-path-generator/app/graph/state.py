from typing import TypedDict, Optional
from app.schemas.resource_schema import Resource
from app.schemas.curriculum_schema import WeekPlan
from app.schemas.planner_schema import LearningSchedule


class GraphState(TypedDict):
    # Initial input parameters
    goal: str
    level: str
    duration_weeks: int

    # Agent structures in the graph state
    resources: Optional[list[Resource]]
    curriculum: Optional[list[WeekPlan]]
    learning_schedule: Optional[LearningSchedule]
