import json

from app.agents.base_agent import BaseAgent
from app.core.errors import FeedbackAgentError
from app.graph.state import ResumeState


class FeedbackAgent(BaseAgent):
    """
    Generates actionable resume improvement feedback based on:
    """

    prompt_file = "feedback_agent.yaml"

    def run(self, state: ResumeState) -> dict:
        self.logger.info("FeedbackAgent started")

        if state.get("error"):
            self.logger.warning("Skipping — upstream error detected")
            return {}

        parsed_sections = state.get("parsed_sections") or {}
        skills_analysis = state.get("skills_analysis") or {}
        scores = state.get("scores") or {}

        try:
            messages = self._build_messages(
                parsed_sections=json.dumps(parsed_sections, indent=2),
                technical_skills=", ".join(skills_analysis.get("technical_skills", [])),
                tools_and_platforms=", ".join(
                    skills_analysis.get("tools_and_platforms", [])
                ),
                domains=", ".join(skills_analysis.get("domains", [])),
                score=scores.get("llm_score", 0),
                missing_skills=", ".join(scores.get("missing_skills", [])) or "None",
                explanation=scores.get("explanation", ""),
                job_description=state.get("job_description") or "Not provided",
            )

            response = self.llm.invoke(messages)

            result = self._parse_json_response(response.content)

            feedback = result.get("feedback", [])

        except Exception as exc:
            self.logger.error(f"Feedback generation failed: {exc}")
            raise FeedbackAgentError(str(exc)) from exc

        self.logger.info(f"Generated {len(feedback)} feedback points")

        return {"feedback": feedback}
