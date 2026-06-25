from langgraph.graph import StateGraph, END
from app.graph.state import ResumeState
from app.agents.parser_agent import ParserAgent
from app.agents.skills_agent import SkillsAgent
from app.agents.scoring_agent import ScoringAgent
from app.agents.feedback_agent import FeedbackAgent
from app.agents.job_fetcher_agent import JobFetcherAgent
from app.core.logger import get_logger

logger = get_logger(__name__)

# Instantiate agents once (they each hold a Groq client)
_parser = ParserAgent()
_skills = SkillsAgent()
_scoring = ScoringAgent()
_feedback = FeedbackAgent()
_job_recommend = JobFetcherAgent()


def parser_node(state: ResumeState) -> dict:
    return _parser.run(state)


def skills_node(state: ResumeState) -> dict:
    return _skills.run(state)


def scoring_node(state: ResumeState) -> dict:
    return _scoring.run(state)


def feedback_node(state: ResumeState) -> dict:
    return _feedback.run(state)


def jobfetcher_node(state: ResumeState) -> dict:
    return _job_recommend.run(state)


def aggregator_node(state: ResumeState) -> dict:
    """
    Combines all outputs into final response.
    """
    parsed_sections = state.get("parsed_sections") or {}
    skills_analysis = state.get("skills_analysis") or {}
    scores = state.get("scores") or {}
    feedback = state.get("feedback") or []
    recommended_jobs = state.get("recommended_jobs") or []

    final_response = {
        "parsed_resume": parsed_sections,
        "skills_analysis": skills_analysis,
        "scores": scores,
        "feedback": feedback,
        "recommended_jobs": recommended_jobs,
    }

    return {"final_response": final_response}


def build_graph():
    graph = StateGraph(ResumeState)

    graph.add_node("parser", parser_node)
    graph.add_node("skills", skills_node)
    graph.add_node("scoring", scoring_node)
    graph.add_node("feedback", feedback_node)
    graph.add_node("job_fetcher", jobfetcher_node)
    graph.add_node("aggregator", aggregator_node)

    graph.set_entry_point("parser")

    graph.add_edge("parser", "skills")
    graph.add_edge("skills", "scoring")
    graph.add_edge("skills", "job_fetcher")

    graph.add_edge("scoring", "feedback")
    graph.add_edge("feedback", "aggregator")
    graph.add_edge("job_fetcher", "aggregator")

    graph.add_edge("aggregator", END)

    return graph.compile()


# Compiled graph — imported by the API route
compiled_graph = build_graph()


def run_analysis(
    extracted_text: str,
    job_description: str | None = None,
) -> dict:
    """
    Run the resume analysis graph on already extracted text.
    """

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

    except Exception:
        logger.exception("Orchestration failed")
        raise
