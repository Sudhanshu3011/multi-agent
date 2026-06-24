class ResumeAnalyserError(Exception):
    """Base exception for the resume analyser."""
    pass


# --- Tool layer ---
class ToolError(ResumeAnalyserError):
    """Raised when a tool invocation fails."""
    pass


class PDFExtractionError(ToolError):
    """Raised when PDF text extraction fails."""
    pass


class SkillMatcherError(ToolError):
    """Raised when skill matching fails."""
    pass


class ScorerError(ToolError):
    """Raised when section scoring fails."""
    pass


# --- Agent layer ---
class AgentError(ResumeAnalyserError):
    """Raised when an agent fails to complete its task."""
    pass


class ParserAgentError(AgentError):
    pass


class SkillsAgentError(AgentError):
    pass


class ScoringAgentError(AgentError):
    pass


class FeedbackAgentError(AgentError):
    pass


class JobRecommendationAgentError(AgentError):
    pass


class OrchestratorError(AgentError):
    """Raised when the LangGraph orchestration fails."""
    pass


# --- API layer ---
class APIError(ResumeAnalyserError):
    """Raised for bad requests or validation failures at the API boundary."""
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.status_code = status_code
