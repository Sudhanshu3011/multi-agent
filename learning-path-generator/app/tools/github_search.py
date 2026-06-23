import json
from langchain_core.tools import tool
from serpapi import GoogleSearch
from app.config import settings


@tool
def github_repo_tool(query: str) -> str:
    """Searches GitHub for open-source repositories, libraries, or codebases matching the query using SerpApi.
    Returns a JSON string list of repository resource dictionaries, each with keys: title, url, description, type.
    """
    if not settings.SERPAPI_API_KEY:
        return json.dumps({"status": "error", "message": "SerpApi API key is missing."})

    try:
        params = {
            "engine": "google",
            "q": f"site:github.com {query}",
            "api_key": settings.SERPAPI_API_KEY,
        }
        search = GoogleSearch(params)
        results_dict = search.get_dict()

        organic_results = results_dict.get("organic_results", [])
        formatted_results = []
        for item in organic_results[:5]:  # Limit to top 5 results
            formatted_results.append(
                {
                    "title": item.get("title", ""),
                    "url": item.get("link", ""),
                    "description": item.get("snippet", "") or "",
                    "type": "Repository",
                }
            )
        return json.dumps(formatted_results)
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})
