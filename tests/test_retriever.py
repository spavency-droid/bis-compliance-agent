from models.product_profile import ProductProfile
from models.standard import BISStandard
from services.retriever import retrieve_candidates


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
    product_name="Battery operated toy car",
    product_type="toy car",
    materials=["plastic"],
    age_group="3-8",
    power_type="rechargeable battery",
    intended_use="children's toy",
    features=["motorized"]
)


results = retrieve_candidates(
    profile,
    standards
)


print("\nCandidate standards:\n")

for result in results:
    print(
        result.standard["standard_id"],
        "-> keyword:",
        round(result.keyword_score, 3),
        "| semantic:",
        round(result.semantic_score, 3),
        "| combined:",
        round(result.combined_score, 3)
    )