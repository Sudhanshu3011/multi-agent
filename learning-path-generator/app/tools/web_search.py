import json
import re
from langchain_core.tools import tool
from tavily import TavilyClient
from app.config import settings


@tool
def tavily_search_tool(query: str) -> str:
    """Searches the web for high-quality online courses, documentation, articles, and tutorials matching the query.
    Returns a JSON string list of resource dictionaries with: title, url, description, type.
    """
    if not settings.TAVILY_API_KEY:
        return json.dumps({"status": "error", "message": "Tavily API key is missing."})

    try:
        client = TavilyClient(api_key=settings.TAVILY_API_KEY)

        response = client.search(query=query, max_results=5, search_depth="basic")

        results = []

        for item in response.get("results", []):
            url = item.get("url", "")
            title = item.get("title", "")

            # Tavily usually provides this as the text snippet
            raw_description = item.get("content", "") or item.get("snippet", "")

            res_type = "Article"
            if "youtube" in url or "video" in url:
                res_type = "Video"
            elif "udemy" in url or "coursera" in url or "course" in url:
                res_type = "Course"
            elif "github" in url:
                res_type = "Repository"
            elif "tutorial" in url or "docs" in url:
                res_type = "Tutorial"

            results.append(
                {
                    "title": title,
                    "url": url,
                    "type": res_type,
                }
            )

        return json.dumps(results)

    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})
