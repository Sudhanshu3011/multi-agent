import json
from langchain_core.tools import tool
from serpapi import GoogleSearch
from app.config import settings

@tool
def youtube_search_tool(query: str) -> str:
    """Searches YouTube for high-quality video tutorials and lectures matching the query.
    Returns a JSON string list of video resource dictionaries, each with keys: title, url, description, type.
    """
    if not settings.SERPAPI_API_KEY:
        return json.dumps({
            "status": "error",
            "message": "SerpApi API key is missing."
        })

    try:
        params = {
            "engine": "youtube",
            "search_query": query,
            "api_key": settings.SERPAPI_API_KEY
        }
        search = GoogleSearch(params)
        results_dict = search.get_dict()
        
        video_results = results_dict.get("video_results", [])
        formatted_results = []
        for item in video_results[:5]:  # Limit to top 5 results
            formatted_results.append({
                "title": item.get("title", ""),
                "url": item.get("link", ""),
                "description": item.get("description", item.get("snippet", "")),
                "type": "Video"
            })
        return json.dumps(formatted_results)
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": str(e)
        })
