from typing import TypedDict, Optional, Dict, Any, List


class ResumeState(TypedDict, total=False):
    extracted_text: str
    job_description: Optional[str]

    parsed_sections: Dict[str, Any]
    skills_analysis: Dict[str, Any]
    scores: Dict[str, Any]

    feedback: List[str]

    job_queries: List[str]
    recommended_jobs: List[Dict[str, Any]]

    final_response: Dict[str, Any]

    error: str
