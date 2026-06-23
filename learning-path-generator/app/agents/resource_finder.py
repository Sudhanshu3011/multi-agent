from typing import List
from app.agents.base_agent import BaseAgent
from app.graph.resource_subgraph import resource_graph
from app.schemas.resource_schema import Resource


class ResourceFinderAgent(BaseAgent):

    def __init__(self):
        super().__init__("resource_finder.yaml")

    def run(self, goal: str, level: str) -> List[Resource]:
        system_prompt = self.prompts.get("system_prompt", "")

        result = resource_graph.invoke(
            {
                "goal": goal,
                "level": level,
                "messages": [
                    ("system", system_prompt),
                    ("user", f"Find resources for {goal} ({level})"),
                ],
            }
        )

        return result["resources"]
