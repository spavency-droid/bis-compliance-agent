from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from graph.state import ComplianceState
from graph.nodes import (
    clarification_node,
    profile_update_node
)


def build_workflow():

    workflow = StateGraph(ComplianceState)

    workflow.add_node(
        "clarification",
        clarification_node
    )

    workflow.add_node(
        "profile_update",
        profile_update_node
    )

    workflow.add_edge(
        START,
        "clarification"
    )

    workflow.add_edge(
        "clarification",
        "profile_update"
    )

    workflow.add_edge(
        "profile_update",
        END
    )

    checkpointer = MemorySaver()

    return workflow.compile(
        checkpointer=checkpointer
    )