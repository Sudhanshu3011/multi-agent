import os
from typing import List, Dict

import requests
from langchain_core.tools import tool
from app.core.config import settings


@tool
def search_google_jobs(
    query: str,
    location: str = "India",
    limit: int = 3,
) -> List[Dict]:
    """
    Search Google Jobs using SerpApi and return a list of jobs.
    """

    params = {
        "engine": "google_jobs",
        "q": query,
        "location": location,
        "api_key": settings.SERPAPI_API_KEY,
    }

    response = requests.get(
        "https://serpapi.com/search",
        params=params,
        timeout=30,
    )
    response.raise_for_status()

    data = response.json()

    jobs = []

    for job in data.get("jobs_results", [])[:limit]:
        jobs.append(
            {
                "title": job.get("title"),
                "company": job.get("company_name"),
                "location": job.get("location"),
                "via": job.get("via"),
                "posted_at": job.get("detected_extensions", {}).get("posted_at"),
            }
        )

    return jobs
