from datetime import datetime


def generate_compliance_report(
    product_description,
    product_profile,
    recommendation,
    match_score,
    next_steps,
):
    """
    Generate a structured compliance summary report.

    The real product profile, recommendation, score,
    and next steps will come from the backend later.
    """

    report = f"""
# BIS Compliance Advisor Report

## 1. Product Description

{product_description}

## 2. Product Profile

- Product Type: {product_profile.get("product_type", "Not available")}
- Category: {product_profile.get("category", "Not available")}
- Material: {product_profile.get("material", "Not available")}
- Power Type: {product_profile.get("power_type", "Not available")}
- Age Group: {product_profile.get("age_group", "Not available")}
- Use Case: {product_profile.get("use_case", "Not available")}

## 3. Recommended Indian Standard

**{recommendation}**

### Match Score

{match_score}

## 4. Next Certification Steps

"""

    for step in next_steps:
        report += f"- {step}\n"

    report += f"""
## 5. Generated

{datetime.now().strftime("%Y-%m-%d %H:%M")}

---

**Important:** This report is an AI-assisted preliminary
compliance assessment and does not constitute official BIS
certification or legal advice. Final applicability should be
verified against the current applicable BIS requirements.
"""

    return report
if __name__ == "__main__":

    test_profile = {
        "product_type": "Toy",
        "category": "Toys",
        "material": "Plastic",
        "power_type": "Battery",
        "age_group": "5-10 years",
        "use_case": "Children's recreational toy",
    }

    test_report = generate_compliance_report(
        product_description="Battery-powered plastic toy for children aged 5-10 years.",
        product_profile=test_profile,
        recommendation="IS 9873",
        match_score=92,
        next_steps=[
            "Verify the applicable scope of the standard.",
            "Check the applicable BIS certification scheme.",
            "Review testing requirements.",
            "Proceed with the applicable BIS certification process.",
        ],
    )

    print(test_report)