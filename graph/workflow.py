from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from graph.state import ComplianceState

from graph.nodes import (
    initial_profile_node,
    clarification_node,
    profile_update_node,
    retrieval_node,
    decision_node,
    route_after_decision
)


def build_workflow():
    workflow = StateGraph(ComplianceState)

    workflow.add_node("initial_profile", initial_profile_node)
    workflow.add_node("clarification", clarification_node)
    workflow.add_node("profile_update", profile_update_node)
    workflow.add_node("retrieval", retrieval_node)
    workflow.add_node("decision", decision_node)

    workflow.add_edge(START, "initial_profile")
    workflow.add_edge("initial_profile", "clarification")
    workflow.add_edge("clarification", "profile_update")
    workflow.add_edge("profile_update", "retrieval")
    workflow.add_edge("retrieval", "decision")

    workflow.add_conditional_edges(
        "decision",
        route_after_decision,
        {
            "continue": "clarification",
            "end": END
        }
    )

    checkpointer = MemorySaver()

    return workflow.compile(checkpointer=checkpointer)