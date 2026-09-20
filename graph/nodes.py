from langgraph.types import interrupt

from agents.clarification_agent import generate_clarification_question
from agents.profile_updater import update_product_profile
from models.product_profile import ProductProfile
from graph.state import ComplianceState

from models.standard import BISStandard
from services.retriever import retrieve_candidates
from services.decision import should_stop, get_stop_reason
from data.standards import DEFAULT_STANDARDS


def _get_profile(state: ComplianceState) -> ProductProfile:

    profile = state["product_profile"]

    if isinstance(profile, ProductProfile):
        return profile

    return ProductProfile(**profile)


def clarification_node(state: ComplianceState):

    profile = _get_profile(state)

    question = generate_clarification_question(
        profile
    )

    user_answer = interrupt({
        "question": question
    })

    return {
        "question": question,
        "user_answer": user_answer,
        "question_count": state["question_count"] + 1
    }


def profile_update_node(state: ComplianceState):

    profile = _get_profile(state)

    updated_profile = update_product_profile(
        profile,
        state["user_answer"]
    )

    return {
        "product_profile": updated_profile.model_dump()
    }


def retrieval_node(state: ComplianceState):

    profile = ProductProfile(
        **state["product_profile"]
    )

    standards = [
        BISStandard(**standard)
        for standard in state["standards"]
    ]

    ranked_results = retrieve_candidates(
        profile,
        standards
    )

    return {
        "ranked_results": ranked_results
    }


def decision_node(state: ComplianceState):

    ranked_results = state["ranked_results"]
    question_count = state["question_count"]

    stop = should_stop(
        ranked_results,
        question_count
    )

    reason = get_stop_reason(
        ranked_results,
        question_count
    )

    if stop:
        print("\nClarification stopped.")
        print("Reason:", reason)

    return {
        "stop_reason": reason
    }


def route_after_decision(state: ComplianceState):

    if should_stop(
        state["ranked_results"],
        state["question_count"]
    ):
        return "end"

    return "continue"