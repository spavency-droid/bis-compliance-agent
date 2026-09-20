from langgraph.types import Command

from models.product_profile import ProductProfile
from models.standard import BISStandard
from graph.workflow import build_workflow


# ---------------------------------------------------------
# Test product
# ---------------------------------------------------------

profile = ProductProfile(
    product_name="toy car",
    product_type="toy car",
    materials=["plastic"],
    age_group="",
    power_type="",
    intended_use="children's toy",
    features=[]
)


# ---------------------------------------------------------
# Test BIS standards
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# Build workflow
# ---------------------------------------------------------

workflow = build_workflow()

config = {
    "configurable": {
        "thread_id": "test-user-1"
    }
}


# ---------------------------------------------------------
# Initial state
# ---------------------------------------------------------

initial_state = {
    "product_profile": profile.model_dump(),
    "question": "",
    "user_answer": "",
    "question_count": 0,
    "standards": [
        standard.model_dump()
        for standard in standards
    ],
    "ranked_results": [],
    "stop_reason": ""
}


# ---------------------------------------------------------
# Start workflow
# ---------------------------------------------------------

result = workflow.invoke(
    initial_state,
    config
)


# ---------------------------------------------------------
# First clarification question
# ---------------------------------------------------------

print("\nWorkflow interrupted.")

interrupt_data = result["__interrupt__"][0].value

print("Question:")
print(interrupt_data["question"])


# ---------------------------------------------------------
# Simulate user's answer
# ---------------------------------------------------------

user_answer = "It uses a rechargeable battery."


result = workflow.invoke(
    Command(resume=user_answer),
    config
)


# ---------------------------------------------------------
# Show updated profile
# ---------------------------------------------------------

print("\nWorkflow resumed.")

print("\nUpdated profile:")
print(ProductProfile(**result["product_profile"]))


# ---------------------------------------------------------
# Show decision result
# ---------------------------------------------------------

print("\nQuestion count:")
print(result["question_count"])

print("\nStop reason:")
print(result["stop_reason"])


# ---------------------------------------------------------
# Show ranked standards
# ---------------------------------------------------------

if result["ranked_results"]:
    print("\nRanked standards:")

    for item in result["ranked_results"]:
        print(
            item.standard["standard_id"],
            "->",
            round(item.combined_score, 3)
        )
else:
    print("\nNo ranked standards found.")
