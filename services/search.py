import json

import numpy as np
from sentence_transformers import SentenceTransformer


# Load the embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def load_standards(path="data/bis_standards.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def to_list(value):
    """
    Convert a dataset field into a list.
    """

    if value is None:
        return []

    if isinstance(value, list):
        return value

    if isinstance(value, str):
        return [
            item.strip()
            for item in value.split(",")
            if item.strip()
        ]

    return []


def profile_value(profile, field, default=""):
    """
    Get a field from either a dictionary or a Pydantic model.
    """

    if isinstance(profile, dict):
        return profile.get(field, default)

    return getattr(profile, field, default)


def build_profile_query(profile):
    """
    Convert ProductProfile into one search query string.
    """

    values = [
        profile_value(profile, "product_name"),
        profile_value(profile, "product_type"),
        " ".join(
            to_list(
                profile_value(profile, "materials")
            )
        ),
        profile_value(profile, "age_group"),
        profile_value(profile, "power_type"),
        profile_value(profile, "intended_use"),
        " ".join(
            to_list(
                profile_value(profile, "features")
            )
        ),
    ]

    return " ".join(
        str(value)
        for value in values
        if value
    ).strip()


def build_standard_text(standard):
    """
    Create searchable text for a BIS standard.
    """

    keywords = to_list(
        standard.get("keywords", [])
    )

    product_types = to_list(
        standard.get("product_types", [])
    )

    materials = to_list(
        standard.get("materials", [])
    )

    return " ".join(
        [
            str(standard.get("title", "")),
            str(standard.get("description", "")),
            " ".join(keywords),
            " ".join(product_types),
            " ".join(materials),
        ]
    )


def build_embeddings(standards):
    """
    Create embeddings for all BIS standards.
    """

    texts = [
        build_standard_text(standard)
        for standard in standards
    ]

    return model.encode(
        texts,
        convert_to_numpy=True
    )


# Load standards and embeddings once
STANDARDS = load_standards()
EMBEDDINGS = build_embeddings(STANDARDS)


def keyword_filter(profile, standards):
    """
    Find standards using structured ProductProfile fields
    and textual keyword matching.
    """

    results = []

    profile_query = build_profile_query(
        profile
    ).lower()

    for standard in standards:

        score = 0
        matched_on = []

        # Power type match
        power_type = profile_value(
            profile,
            "power_type"
        )

        power_types = [
            item.lower()
            for item in to_list(
                standard.get("power_types", [])
            )
        ]

        if (
            power_type
            and str(power_type).lower() in power_types
        ):
            score += 1
            matched_on.append("power_type")

        # Age group match
        age_group = profile_value(
            profile,
            "age_group"
        )

        age_groups = [
            item.lower()
            for item in to_list(
                standard.get("age_groups", [])
            )
        ]

        if (
            age_group
            and str(age_group).lower() in age_groups
        ):
            score += 1
            matched_on.append("age_group")

        # Keyword matches
        keywords = to_list(
            standard.get("keywords", [])
        )

        keyword_matches = [
            keyword
            for keyword in keywords
            if keyword.lower() in profile_query
        ]

        score += len(keyword_matches)
        matched_on.extend(keyword_matches)

        if score > 0:
            results.append(
                {
                    "standard": standard,
                    "kw_score": score,
                    "matched_on": matched_on
                }
            )

    return results


def semantic_search(
    query,
    standards,
    embeddings,
    top_k=20
):
    """
    Find standards using semantic similarity.
    """

    if not query:
        return []

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    )[0]

    denominator = (
        np.linalg.norm(
            embeddings,
            axis=1
        )
        * np.linalg.norm(query_embedding)
    )

    similarities = np.dot(
        embeddings,
        query_embedding
    ) / denominator

    ranked_indices = np.argsort(
        -similarities
    )[:top_k]

    return [
        (
            standards[index],
            float(similarities[index])
        )
        for index in ranked_indices
    ]


def search_standards(
    product_profile,
    top_k=5
):
    """
    Retrieve the most relevant BIS standards
    for a ProductProfile.

    Combines keyword filtering and semantic search.
    """

    query = build_profile_query(
        product_profile
    )

    # Keyword search
    keyword_results = keyword_filter(
        product_profile,
        STANDARDS
    )

    # Semantic search
    semantic_results = semantic_search(
        query,
        STANDARDS,
        EMBEDDINGS,
        top_k=20
    )

    combined = {}

    # Keyword contribution = 30%
    for result in keyword_results:

        standard = result["standard"]
        standard_id = standard["standard_id"]

        combined[standard_id] = {
            "standard": standard,
            "score": result["kw_score"] * 0.3,
            "matched_on": result["matched_on"]
        }

    # Semantic contribution = 70%
    for standard, similarity in semantic_results:

        standard_id = standard["standard_id"]

        if standard_id in combined:

            combined[standard_id]["score"] += (
                similarity * 0.7
            )

        else:

            combined[standard_id] = {
                "standard": standard,
                "score": similarity * 0.7,
                "matched_on": []
            }

    # Rank results
    ranked = sorted(
        combined.values(),
        key=lambda x: -x["score"]
    )[:top_k]

    # Normalize scores
    max_score = max(
        (
            result["score"]
            for result in ranked
        ),
        default=1
    )

    final_results = []

    for result in ranked:

        normalized_score = round(
            result["score"] / max_score,
            3
        )

        final_results.append(
            {
                "standard_id":
                    result["standard"]["standard_id"],

                "title":
                    result["standard"]["title"],

                "score":
                    normalized_score,

                "matched_on":
                    result["matched_on"],

                "category":
                    result["standard"]["category"]
            }
        )

    return final_results


# --------------------------------------------------
# Test
# --------------------------------------------------

if __name__ == "__main__":

    test_profile = {
        "product_name": "Cotton clothing fabric",
        "product_type": "textile fabric",
        "materials": ["cotton"],
        "age_group": "",
        "power_type": "",
        "intended_use": "clothing",
        "features": ["woven", "fabric"]
    }

    results = search_standards(
        test_profile,
        top_k=5
    )

    print("\nFinal search results:")

    for result in results:

        print(
            result["standard_id"],
            "| score:",
            result["score"],
            "| category:",
            result["category"],
            "| matched:",
            result["matched_on"],
            "|",
            result["title"]
        )