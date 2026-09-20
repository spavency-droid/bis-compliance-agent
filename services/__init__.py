from models.product_profile import ProductProfile
from models.standard import BISStandard
from models.retrieval import RetrievalResult


def keyword_score(
    profile: ProductProfile,
    standard: BISStandard
) -> float:

    profile_terms = set()

    if profile.product_type:
        profile_terms.add(profile.product_type.lower())

    for material in profile.materials:
        profile_terms.add(material.lower())

    if profile.power_type:
        profile_terms.add(profile.power_type.lower())

    if profile.age_group:
        profile_terms.add(profile.age_group.lower())

    if profile.intended_use:
        profile_terms.add(profile.intended_use.lower())

    for feature in profile.features:
        profile_terms.add(feature.lower())

    standard_terms = set()

    for value in standard.product_types:
        standard_terms.add(value.lower())

    for value in standard.materials:
        standard_terms.add(value.lower())

    for value in standard.power_types:
        standard_terms.add(value.lower())

    for value in standard.age_groups:
        standard_terms.add(value.lower())

    for value in standard.use_cases:
        standard_terms.add(value.lower())

    for value in standard.keywords:
        standard_terms.add(value.lower())

    if not profile_terms or not standard_terms:
        return 0.0

    matches = profile_terms.intersection(standard_terms)

    return len(matches) / len(profile_terms)


def retrieve_candidates(
    profile: ProductProfile,
    standards: list[BISStandard]
) -> list[RetrievalResult]:

    results = []

    for standard in standards:

        score = keyword_score(
            profile,
            standard
        )

        results.append(
            RetrievalResult(
                standard=standard.model_dump(),
                keyword_score=score,
                semantic_score=0.0,
                combined_score=score
            )
        )

    results.sort(
        key=lambda result: result.combined_score,
        reverse=True
    )

    return results
