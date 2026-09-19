from models.product_profile import ProductProfile
from graph.workflow import build_workflow


profile = ProductProfile(
    product_name="toy car",
    product_type="toy car",
    materials=["plastic"],
    age_group="",
    power_type="",
    intended_use="children's toy",
    features=[]
)


workflow = build_workflow()


initial_state = {
    "product_profile": profile,
    "question": "",
    "user_answer": "It uses a rechargeable battery.",
    "question_count": 0
}


result = workflow.invoke(initial_state)


print("\nQuestion:")
print(result["question"])

print("\nUpdated profile:")
print(result["product_profile"])
