from typing import TypedDict


class ComplianceState(TypedDict):
    product_profile: dict
    question: str
    user_answer: str
    question_count: int