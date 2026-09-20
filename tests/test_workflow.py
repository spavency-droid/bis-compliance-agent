from models.product_profile import ProductProfile
from graph.workflow import build_workflow


profile = ProductProfile(
    product_name="toy car",
    product_type="toy car",
    materials=["plastic"],
    age_group="",
    power_type="rechargeable battery",
    intended_use="children's toy",
    features=[]
)


workflow = build_workflow()


initial_state = {
    "product_profile": profile.model_dump(),
    "question": "",
    "user_answer": "It uses a rechargeable battery.",
    "question_count": 0,
    "ranked_results": [],
    "stop_reason": ""
}


result = workflow.invoke(
    initial_state,
    config={
        "configurable": {
            "thread_id": "test-thread-1"
        }
    }
)


print("\nQuestion:")
print(result["question"])

print("\nUpdated profile:")
print(result["product_profile"])

print("\nQuestion count:")
print(result["question_count"])

print("\nStop reason:")
print(result["stop_reason"])