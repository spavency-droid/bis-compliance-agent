from langgraph.types import Command

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


config = {
    "configurable": {
        "thread_id": "test-user-1"
    }
}


initial_state = {
    "product_profile": profile.model_dump(),
    "question": "",
    "user_answer": "",
    "question_count": 0
}


# Start the workflow
result = workflow.invoke(
    initial_state,
    config
)


print("\nWorkflow interrupted.")
print("Question:")
print(result["__interrupt__"][0].value["question"])


# Simulate user's answer
user_answer = "It uses a rechargeable battery."


result = workflow.invoke(
    Command(resume=user_answer),
    config
)


print("\nWorkflow resumed.")

print("\nUpdated profile:")
print(ProductProfile(**result["product_profile"]))