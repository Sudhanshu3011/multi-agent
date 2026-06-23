import logging
from typing import List
from langchain_core.output_parsers import JsonOutputParser
from app.agents.base_agent import BaseAgent, InvalidLLMResponseError
from app.schemas.planner_schema import LearningSchedule
from app.schemas.curriculum_schema import WeekPlan
from app.schemas.resource_schema import Resource
from app.tools.utils import format_resources, format_curriculum

logger = logging.getLogger(__name__)


class PlannerAgent(BaseAgent):
    """
    Intelligent planner agent that creates a structured learning schedule with
    step-by-step progression, phase impacts, and proper flow guidance.
    """

    def __init__(self):
        super().__init__("planner.yaml")

    def run(
        self,
        goal: str,
        level: str,
        duration_weeks: int,
        resources: List[Resource],
        curriculum: List[WeekPlan],
    ) -> LearningSchedule:
        """
        Generates a comprehensive learning schedule with phases, phase impacts,
        and step-by-step progression guidance.
        """
        llm = self.get_llm()

        parser = JsonOutputParser(pydantic_object=LearningSchedule)
        format_instructions = parser.get_format_instructions()

        system_p = self.prompts.get("system_prompt", "") + f"\n\n{format_instructions}"
        user_p = self.prompts.get("user_prompt_template", "").format(
            goal=goal,
            level=level,
            duration_weeks=duration_weeks,
            resources=format_resources(resources),
            curriculum=format_curriculum(curriculum),
        )

        try:
            chain = llm | parser
            parsed_dict = chain.invoke([("system", system_p), ("user", user_p)])
            return LearningSchedule(**parsed_dict)

        except Exception as exc:
            raise InvalidLLMResponseError(
                f"PlannerAgent failed to get valid structured response: {exc}"
            )
