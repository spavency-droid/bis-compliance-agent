from models.product_profile import ProductProfile
from models.standard import BISStandard
from models.retrieval import RetrievalResult

from services.semantic_search import SemanticSearcher
from services.vector_search import VectorSearcher


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


def standard_to_text(standard: BISStandard) -> str:

    return " ".join([
        standard.title,
        standard.category,
        " ".join(standard.product_types),
        " ".join(standard.materials),
        " ".join(standard.power_types),
        " ".join(standard.age_groups),
        " ".join(standard.use_cases),
        " ".join(standard.keywords),
        standard.scope
    ])


def profile_to_text(profile: ProductProfile) -> str:

    return " ".join([
        profile.product_name,
        profile.product_type,
        " ".join(profile.materials),
        profile.age_group,
        profile.power_type,
        profile.intended_use,
        " ".join(profile.features)
    ])


def retrieve_candidates(
    profile: ProductProfile,
    standards: list[BISStandard]
) -> list[RetrievalResult]:

    if not standards:
        return []

    semantic_searcher = SemanticSearcher()

    standard_texts = [
        standard_to_text(standard)
        for standard in standards
    ]

    standard_embeddings = semantic_searcher.encode(
        standard_texts
    )

    vector_searcher = VectorSearcher(
        standard_embeddings
    )

    profile_text = profile_to_text(profile)

    profile_embedding = semantic_searcher.encode(
        [profile_text]
    )[0]

    scores, indices = vector_searcher.search(
        profile_embedding,
        top_k=len(standards)
    )

    semantic_scores = {}

    for score, index in zip(scores, indices):
        semantic_scores[index] = float(score)

    results = []

    for index, standard in enumerate(standards):

        k_score = keyword_score(
            profile,
            standard
        )

        s_score = semantic_scores.get(
            index,
            0.0
        )

        combined_score = (
            0.6 * k_score
            + 0.4 * s_score
        )

        results.append(
            RetrievalResult(
                standard=standard.model_dump(),
                keyword_score=k_score,
                semantic_score=s_score,
                combined_score=combined_score
            )
        )

    results.sort(
        key=lambda result: result.combined_score,
        reverse=True
    )

    return results