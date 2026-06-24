from langchain_core.messages import ToolMessage

from app.agents.base_agent import BaseAgent
from app.core.errors import JobRecommendationAgentError
from app.graph.state import ResumeState
from app.tools.job_search import search_google_jobs


class JobRecommendationAgent(BaseAgent):

    prompt_file = "job_recommendation_agent.yaml"

    def __init__(self):
        super().__init__()

        self.tools = [search_google_jobs]
        self.llm_with_tools = self.llm.bind_tools(self.tools)

        self.tool_map = {tool.name: tool for tool in self.tools}

    def run(self, state: ResumeState) -> dict:
        self.logger.info("JobRecommendationAgent started")

        if state.get("error"):
            self.logger.warning("Skipping due to upstream error.")
            return {}

        try:
            skills_analysis = state.get(
                "skills_analysis",
                {},
            )

            messages = self._build_messages(
                technical_skills=", ".join(
                    skills_analysis.get(
                        "technical_skills",
                        [],
                    )
                ),
                tools_and_platforms=", ".join(
                    skills_analysis.get(
                        "tools_and_platforms=",
                        [],
                    )
                ),
                domains=", ".join(
                    skills_analysis.get(
                        "domains",
                        [],
                    )
                ),
            )

            response = self.llm_with_tools.invoke(messages)

            tool_messages = []

            for tool_call in response.tool_calls:

                tool_name = tool_call["name"]

                tool = self.tool_map[tool_name]

                tool_result = tool.invoke(tool_call["args"])

                tool_messages.append(
                    ToolMessage(
                        content=str(tool_result),
                        tool_call_id=tool_call["id"],
                    )
                )

            final_response = self.llm_with_tools.invoke(
                messages + [response] + tool_messages
            )

            result = self._parse_json_response(final_response.content)

            self.logger.info("Job recommendations generated")

            return {"recommended_jobs": result.get("recommended_jobs", [])}

        except Exception as exc:
            self.logger.exception("Job recommendation failed")

            raise JobRecommendationAgentError(str(exc)) from exc
