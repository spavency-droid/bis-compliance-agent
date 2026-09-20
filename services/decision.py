MAX_QUESTIONS = 4
EARLY_EXIT_MARGIN = 0.15


def should_stop(
    ranked_results,
    questions_asked: int
) -> bool:

    # Safety check
    if not ranked_results:
        return False

    # Mandatory question budget
    if questions_asked >= MAX_QUESTIONS:
        return True

    # Need at least two candidates
    if len(ranked_results) < 2:
        return True

    top_score = ranked_results[0].combined_score
    runner_up_score = ranked_results[1].combined_score

    margin = top_score - runner_up_score

    return margin >= EARLY_EXIT_MARGIN

def get_stop_reason(
    ranked_results,
    questions_asked: int
) -> str:

    if questions_asked >= MAX_QUESTIONS:
        return (
            "Stopped because the maximum of "
            "4 clarification questions was reached."
        )

    if len(ranked_results) < 2:
        return (
            "Stopped because only one viable "
            "standard candidate was found."
        )

    top_score = ranked_results[0].combined_score
    runner_up_score = ranked_results[1].combined_score

    margin = top_score - runner_up_score

    if margin >= EARLY_EXIT_MARGIN:
        return (
            f"Stopped early because the top candidate "
            f"leads the runner-up by {margin:.2f}, "
            f"which meets the required margin of "
            f"{EARLY_EXIT_MARGIN:.2f}."
        )

    return "More clarification is required."

