from typing import List
from app.schemas.resource_schema import Resource
from app.schemas.curriculum_schema import WeekPlan


def format_resources(resources: List[Resource]) -> str:
    """Format resources into a readable string."""
    if not resources:
        return "No resources found."

    formatted = []
    for res in resources:
        formatted.append(
            f"- {res.title} ({res.type}): [URL: {res.url}] "
            f"[Rating: {res.rating or 'N/A'}/5]"
        )
    return "\n".join(formatted)


def format_curriculum(curriculum: List[WeekPlan]) -> str:
    """Format curriculum into a readable string."""
    if not curriculum:
        return "No curriculum structure provided."

    formatted = []
    for week in curriculum:
        topics = ", ".join(week.topics)
        formatted.append(f"Week {week.week}: {topics} (~{week.estimated_hours} hours)")
    return "\n".join(formatted)
