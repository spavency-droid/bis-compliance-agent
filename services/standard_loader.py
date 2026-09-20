import json

from models.standard import BISStandard


def to_list(value):
    if value is None:
        return []

    if isinstance(value, list):
        return value

    if isinstance(value, str):
        return [
            item.strip()
            for item in value.replace(";", ",").split(",")
            if item.strip()
        ]

    return []


def load_standards(path="data/bis_standards.json"):
    with open(path, "r", encoding="utf-8") as f:
        records = json.load(f)

    standards = []

    for record in records:
        standard = BISStandard(
            standard_id=record.get("standard_id", ""),
            title=record.get("title", ""),
            category=record.get("category", ""),
            product_types=to_list(record.get("product_types")),
            materials=to_list(record.get("materials")),
            power_types=to_list(record.get("power_types")),
            age_groups=to_list(record.get("age_groups")),
            use_cases=[],
            keywords=to_list(record.get("keywords")),
            scope=record.get("description", ""),
            certification_scheme=record.get("certification_notes", ""),
            mandatory_status="",
            source_url=record.get("source", ""),
            source_date="",
        )

        standards.append(standard)

    return standards