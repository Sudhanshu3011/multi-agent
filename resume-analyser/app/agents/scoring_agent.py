from app.agents.base_agent import BaseAgent
from app.core.errors import ScoringAgentError
from app.graph.state import ResumeState


class ScoringAgent(BaseAgent):

    prompt_file = "scoring_agent.yaml"

    def run(self, state: ResumeState) -> dict:
        self.logger.info("ScoringAgent started")

        if state.get("error"):
            self.logger.warning("Skipping — upstream error detected")
            return {}

        parsed_sections = state.get("parsed_sections") or {}

        experience = parsed_sections.get("experience", "")
        skills_analysis = state.get("skills_analysis", {})
        job_description = state.get("job_description", "")

        try:

            messages = self._build_messages(
                technical_skills=skills_analysis.get("technical_skills", []),
                tools_and_platforms=skills_analysis.get("tools_and_platforms", []),
                domains=skills_analysis.get("domains", []),
                experience=experience,
                job_description=job_description,
            )

            response = self.llm.invoke(messages)

            llm_evaluation = self._parse_json_response(response.content)

            scores = {
                "llm_score": llm_evaluation.get("score"),
                "missing_skills": llm_evaluation.get("missing_skills", []),
                "explanation": llm_evaluation.get("explanation", ""),
            }

        except Exception as exc:
            self.logger.warning(f"LLM interpretation failed: {exc}")

            scores = {
                "llm_score": None,
                "missing_skills": [],
                "explanation": "LLM evaluation failed",
            }

        return {"scores": scores}
