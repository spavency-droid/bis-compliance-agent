from models.product_profile import ProductProfile
from agents.profile_updater import update_product_profile


profile = ProductProfile(
    product_name="toy car",
    product_type="toy car",
    materials=["plastic"],
    age_group="",
    power_type="",
    intended_use="children's toy",
    features=[]
)


updated_profile = update_product_profile(
    profile,
    "Yes, it is electrically powered and uses a rechargeable battery."
)


print("\nUpdated profile:")
print(updated_profile)