from typing import Dict, Any
from langgraph.graph import StateGraph, START, END

from app.graph.state import GraphState
from app.agents.resource_finder import ResourceFinderAgent
from app.agents.curriculum_agent import CurriculumAgent
from app.agents.planner_agent import PlannerAgent

# ── Nodes ──────────────────────────────────────────────────────────────────────

def resource_finder_node(state: GraphState) -> Dict[str, Any]:
    agent = ResourceFinderAgent()
    goal = state.get("goal", "")
    level = state.get("level", "beginner")
    result = agent.run(goal=goal, level=level)
    return {"resources": result}


def curriculum_node(state: GraphState) -> Dict[str, Any]:
    agent = CurriculumAgent()
    goal = state.get("goal", "")
    level = state.get("level", "beginner")
    duration_weeks = state.get("duration_weeks", 8)
    resources = state.get("resources") or []
    result = agent.run(
        goal=goal,
        level=level,
        duration_weeks=duration_weeks,
        resources=resources,
    )
    return {"curriculum": result}


def planner_node(state: GraphState) -> Dict[str, Any]:
    agent = PlannerAgent()
    goal = state.get("goal", "")
    level = state.get("level", "beginner")
    duration_weeks = state.get("duration_weeks", 8)
    result = agent.run(
        goal=goal,
        level=level,
        duration_weeks=duration_weeks,
        resources=state.get("resources") or [],
        curriculum=state.get("curriculum") or [],
    )
    return {"learning_schedule": result}

# ── Edges ──────────────────────────────────────────────────────────────────────

def build_graph_edges(workflow: StateGraph) -> None:
    """Configures routing edges to the graph workflow."""
    # Sequential execution: START -> resource_finder -> curriculum -> planner -> END
    workflow.add_edge(START, "resource_finder")
    workflow.add_edge("resource_finder", "curriculum")
    workflow.add_edge("curriculum", "planner")
    workflow.add_edge("planner", END)

# ── Pipeline Construction ──────────────────────────────────────────────────────

def compile_pipeline() -> StateGraph:
    """Builds and compiles the complete modular StateGraph pipeline."""
    workflow = StateGraph(GraphState)
    
    # Register Nodes
    workflow.add_node("resource_finder", resource_finder_node)
    workflow.add_node("curriculum", curriculum_node)
    workflow.add_node("planner", planner_node)
    
    # Register Edges
    build_graph_edges(workflow)
    
    return workflow.compile()

# Compile the modular graph instance directly here
graph_app = compile_pipeline()
