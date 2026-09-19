from langgraph.types import interrupt

from agents.clarification_agent import generate_clarification_question
from agents.profile_updater import update_product_profile
from models.product_profile import ProductProfile
from graph.state import ComplianceState


def clarification_node(state: ComplianceState):

    profile = ProductProfile(
        **state["product_profile"]
    )

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

    profile = ProductProfile(
        **state["product_profile"]
    )

    updated_profile = update_product_profile(
        profile,
        state["user_answer"]
    )

    return {
        "product_profile": updated_profile.model_dump()
    }