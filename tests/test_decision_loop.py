from models.product_profile import ProductProfile
from models.standard import BISStandard

from graph.nodes import retrieval_node, decision_node

from graph.state import ComplianceState


standards = [
    BISStandard(
        standard_id="TEST-TOY-001",
        title="Toy Safety Standard - Test Record",
        category="Toys",
        product_types=["toy car"],
        materials=["plastic"],
        power_types=["rechargeable battery"],
        age_groups=["3-8"],
        use_cases=["children's toy"],
        keywords=["toy", "car", "motorized"]
    ),

    BISStandard(
        standard_id="TEST-TEXTILE-001",
        title="Textile Product Standard - Test Record",
        category="Textiles",
        product_types=["shirt"],
        materials=["cotton"],
        keywords=["clothing", "textile"]
    ),

    BISStandard(
        standard_id="TEST-PACKAGING-001",
        title="Food Packaging Standard - Test Record",
        category="Food Packaging",
        product_types=["food container"],
        materials=["plastic"],
        use_cases=["food packaging"],
        keywords=["container", "packaging"]
    )
]


profile = ProductProfile(
    product_name="toy car",
    product_type="toy car",
    materials=["plastic"],
    age_group="3-8",
    power_type="rechargeable battery",
    intended_use="children's toy",
    features=["motorized", "wheels"]
)


state: ComplianceState = {

    "product_profile": profile.model_dump(),

    "question": "",

    "user_answer": "",

    "question_count": 1,

    "standards": [
        standard.model_dump()
        for standard in standards
    ],

    "ranked_results": [],

    "stop_reason": ""
}


print("Running retrieval...")

retrieval_result = retrieval_node(state)

state.update(retrieval_result)


print("\nRanked results:")

for result in state["ranked_results"]:

    print(
        result.standard["standard_id"],
        "->",
        round(result.combined_score, 3)
    )


print("\nRunning decision...")

decision_result = decision_node(state)

state.update(decision_result)


print("\nStop reason:")

print(state["stop_reason"])