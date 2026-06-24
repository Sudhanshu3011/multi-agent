import os
from typing import List, Dict

import requests
from langchain_core.tools import tool
from app.core.config import get_settings


@tool
def search_google_jobs(
    query: str,
    location: str = "India",
    limit: int = 10,
) -> List[Dict]:
    """
    Search Google Jobs using SerpApi and return a list of jobs.
    """

    settings = get_settings()

    params = {
        "engine": "google_jobs",
        "q": query,
        "location": location,
        "api_key": settings.serpapi_api_key,
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
                "description": job.get("description"),
                "via": job.get("via"),
                "posted_at": job.get("detected_extensions", {}).get("posted_at"),
                "thumbnail": job.get("thumbnail"),
                "apply_links": [
                    link.get("link")
                    for link in job.get("related_links", [])
                    if link.get("link")
                ],
            }
        )

    return jobs
