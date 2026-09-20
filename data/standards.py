from models.standard import BISStandard


DEFAULT_STANDARDS = [
    BISStandard(
        standard_id="TEST-TOY-001",
        title="Toy Safety Standard - Test Record",
        category="Toys",
        product_types=["toy car"],
        materials=["plastic"],
        power_types=["rechargeable battery"],
        age_groups=["3-8"],
        use_cases=["children's toy"],
        keywords=["toy", "car", "motorized"],
    ),
    BISStandard(
        standard_id="TEST-TEXTILE-001",
        title="Textile Product Standard - Test Record",
        category="Textiles",
        product_types=["shirt"],
        materials=["cotton"],
        keywords=["clothing", "textile"],
    ),
    BISStandard(
        standard_id="TEST-PACKAGING-001",
        title="Food Packaging Standard - Test Record",
        category="Food Packaging",
        product_types=["food container"],
        materials=["plastic"],
        use_cases=["food packaging"],
        keywords=["container", "packaging"],
    ),
]
