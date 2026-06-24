from app.agents.base_agent import BaseAgent
from app.graph.state import ResumeState


class SkillsAgent(BaseAgent):

    prompt_file = "skills_agent.yaml"

    def run(self, state: ResumeState) -> dict:
        self.logger.info("SkillsAgent started")

        if state.get("error"):
            self.logger.warning("Skipping — upstream error detected")
            return {}

        parsed_sections = state.get("parsed_sections") or {}

        experience = parsed_sections.get("experience", "")
        skills = parsed_sections.get("skills", "")
        projects = parsed_sections.get("projects", "")
        certifications = parsed_sections.get("certifications", "")

        try:
            messages = self._build_messages(
                experience=experience,
                skills=skills,
                projects=projects,
                certifications=certifications,
            )

            response = self.llm.invoke(messages)

            enriched = self._parse_json_response(response.content)

        except Exception as exc:
            self.logger.warning(f"LLM enrichment failed, using fallback only: {exc}")
            enriched = {}

        skills_analysis = {
            "technical_skills": enriched.get("technical_skills", []),
            "tools_and_platforms": enriched.get("tools_and_platforms", []),
            "domains": enriched.get("domains", []),
        }

        return {"skills_analysis": skills_analysis}
