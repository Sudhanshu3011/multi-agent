from langgraph.graph import StateGraph, END
from app.graph.state import ResumeState
from app.agents.parser_agent import ParserAgent
from app.agents.skills_agent import SkillsAgent

from app.agents.scoring_agent import ScoringAgent

from app.agents.feedback_agent import FeedbackAgent

# from app.agents.job_recommendation import JobRecommendationAgent

from app.core.errors import OrchestratorError
from app.core.logger import get_logger
from app.tools.pdf_extractor import extract_text

logger = get_logger(__name__)

# Instantiate agents once (they each hold a Groq client)
_parser = ParserAgent()
_skills = SkillsAgent()
_scoring = ScoringAgent()
_feedback = FeedbackAgent()
# _job_recommend = JobRecommendationAgent()


def parser_node(state: ResumeState) -> dict:
    return _parser.run(state)


def skills_node(state: ResumeState) -> dict:
    return _skills.run(state)


def scoring_node(state: ResumeState) -> dict:
    return _scoring.run(state)


def feedback_node(state: ResumeState) -> dict:
    return _feedback.run(state)


# def jobrecommendation_node(state: ResumeState) -> dict:
#     return _job_recommend.run(state)


def build_graph():
    graph = StateGraph(ResumeState)

    graph.add_node("parser", parser_node)
    graph.add_node("skills", skills_node)
    graph.add_node("scoring", scoring_node)
    graph.add_node("feedback", feedback_node)
    # graph.add_node("job_recommend", jobrecommendation_node)

    graph.set_entry_point("parser")

    graph.add_edge("parser", "skills")
    graph.add_edge("skills", "scoring")

    graph.add_edge("scoring", "feedback")

    # Final node
    graph.add_edge("feedback", END)

    return graph.compile()


# Compiled graph — imported by the API route
compiled_graph = build_graph()


def run_analysis(pdf_bytes: bytes, job_description: str | None = None) -> dict:
    """
    Entry point called by the API route.
    Returns the final ResumeState as a dict.
    """
    try:
        extracted_text = extract_text(pdf_bytes)
    except Exception as exc:
        logger.error(f"PDF extraction failed: {exc}")
        raise OrchestratorError(f"PDF extraction failed: {exc}") from exc

    initial_state: ResumeState = {
        "extracted_text": extracted_text,
        "job_description": job_description,
        "parsed_sections": None,
        "skills_analysis": {
            "technical_skills": [],
            "tools_and_platforms": [],
            "domains": [],
        },
        "scores": None,
        "feedback": None,
        "error": None,
    }

    try:
        logger.info("Starting resume analysis pipeline")
        final_state = compiled_graph.invoke(initial_state)
        logger.info("Pipeline completed successfully")
        return final_state
    except Exception as exc:
        logger.error(f"Orchestration failed: {exc}")
        raise OrchestratorError(str(exc)) from exc
