from models.product_profile import ProductProfile


profile = ProductProfile(
    product_name="Battery-operated toy car",
    product_type="toy car",
    materials=["plastic", "metal"],
    age_group="3-8",
    power_type="battery",
    intended_use="children's toy",
    features=["motorized", "remote control"]
)

print(profile)