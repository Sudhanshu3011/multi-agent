from typing import Annotated, TypedDict
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.output_parsers import JsonOutputParser

from app.config import settings
from app.tools.web_search import tavily_search_tool
from app.tools.youtube_search import youtube_search_tool
from app.tools.github_search import github_repo_tool
from app.schemas.resource_schema import ResourceList


# Define a state for the resource agent
class ResourceState(TypedDict):
    messages: Annotated[list, add_messages]
    resources: list
    goal: str
    level: str


# Create the tools
TOOLS = [tavily_search_tool, youtube_search_tool, github_repo_tool]


# Create the LLM
def _get_llm() -> ChatGroq:
    return ChatGroq(
        temperature=settings.LLM_TEMPERATURE,
        groq_api_key=settings.GROQ_API_KEY,
        model_name=settings.LLM_MODEL,
    )


llm = _get_llm()
llm_with_tools = llm.bind_tools(TOOLS)


# Create the agent node
def agent_node(state: ResourceState) -> dict:
    """Agent node that queries LLM bound with YouTube, GitHub, and Tavily tools."""
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}


# Create ToolNode
tool_node = ToolNode(TOOLS)

# Create the formatter node
parser = JsonOutputParser(pydantic_object=ResourceList)
format_instructions = parser.get_format_instructions()


def formatter_node(state: ResourceState) -> dict:
    """Formatter node that structures the search agent conversation into a ResourceList."""
    # Serialize the conversation history content to avoid message-type tool conflicts
    conversation_text = ""
    for msg in state["messages"]:
        if hasattr(msg, "content") and msg.content:
            role = "Assistant" if msg.type == "ai" else msg.type.capitalize()
            conversation_text += f"{role}: {msg.content}\n"

    system_prompt = f"""
    You are an expert technical educator and resource curator.

    User Goal:
    {state["goal"]}

    Experience Level:
    {state["level"]}

    Analyze the search results and identify the most relevant learning resources.

    For each resource generate:

    1. title
    2. url
    3. type

    Do not simply copy snippets from search results.

    Avoid duplicate resources.

    Prefer:
    - Official documentation
    - Well-maintained GitHub repositories
    - High-quality YouTube videos
    - Structured courses

    {format_instructions}
    """

    chain = llm | parser
    parsed_dict = chain.invoke(
        [
            ("system", system_prompt),
            (
                "user",
                f"Here is the conversation text containing search results:\n\n{conversation_text}",
            ),
        ]
    )
    result = ResourceList(**parsed_dict)
    return {"resources": result.resources}


# Build the resource graph
builder = StateGraph(ResourceState)

builder.add_node("agent", agent_node)
builder.add_node("tools", tool_node)
builder.add_node("formatter", formatter_node)

# Edges
builder.add_edge(START, "agent")

builder.add_conditional_edges(
    "agent", tools_condition, {"tools": "tools", "__end__": "formatter"}
)

builder.add_edge("tools", "agent")
builder.add_edge("formatter", END)

# Compile
resource_graph = builder.compile()
