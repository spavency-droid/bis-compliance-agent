from typing import TypedDict

from models.standard import BISStandard


class ComplianceState(TypedDict):

    product_profile: dict

    standards: list[BISStandard]

    question: str

    user_answer: str

    question_count: int

    ranked_results: list

    stop_reason: str