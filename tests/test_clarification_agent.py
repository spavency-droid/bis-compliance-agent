from models.product_profile import ProductProfile
from agents.clarification_agent import generate_clarification_question


profile = ProductProfile(
    product_name="Battery-operated toy car",
    product_type="toy car",
    materials=["plastic"],
    age_group="",
    power_type="battery",
    intended_use="children's toy",
    features=["remote control", "motorized"]
)


question = generate_clarification_question(profile)

print("\nGenerated question:")
print(question)