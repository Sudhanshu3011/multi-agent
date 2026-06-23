import logging
from typing import List
from langchain_core.output_parsers import JsonOutputParser
from app.agents.base_agent import BaseAgent, InvalidLLMResponseError
from app.schemas.curriculum_schema import LearningPlan, WeekPlan
from app.schemas.resource_schema import Resource
from app.tools.utils import format_resources

logger = logging.getLogger(__name__)


class CurriculumAgent(BaseAgent):
    def __init__(self):
        super().__init__("curriculum.yaml")

    def run(
        self,
        goal: str,
        level: str,
        duration_weeks: int,
        resources: List[Resource] = None,
    ) -> List[WeekPlan]:
        """
        Generates a week-by-week curriculum utilizing provided resources.
        """
        llm = self.get_llm()

        parser = JsonOutputParser(pydantic_object=LearningPlan)
        format_instructions = parser.get_format_instructions()

        resources_formatted = format_resources(resources or [])

        system_p = self.prompts.get("system_prompt", "") + f"\n\n{format_instructions}"
        user_p = self.prompts.get("user_prompt_template", "").format(
            goal=goal,
            level=level,
            duration_weeks=duration_weeks,
            resources=resources_formatted,
        )

        try:
            chain = llm | parser
            parsed_dict = chain.invoke([("system", system_p), ("user", user_p)])
            parsed_result = LearningPlan(**parsed_dict)
            return parsed_result.curriculum

        except Exception as exc:
            raise InvalidLLMResponseError(
                f"CurriculumAgent failed to get valid structured response: {exc}"
            )
