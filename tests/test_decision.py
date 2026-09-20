from services.decision import (
    should_stop,
    get_stop_reason
)


class FakeResult:

    def __init__(self, score):
        self.combined_score = score


# Strong winner
results = [
    FakeResult(0.82),
    FakeResult(0.60),
    FakeResult(0.40)
]

print("Strong winner:")
print("Should stop:", should_stop(results, 1))
print("Reason:", get_stop_reason(results, 1))


# Close candidates
results = [
    FakeResult(0.68),
    FakeResult(0.60),
    FakeResult(0.40)
]

print("\nClose candidates:")
print("Should stop:", should_stop(results, 1))
print("Reason:", get_stop_reason(results, 1))


# Four questions reached
results = [
    FakeResult(0.68),
    FakeResult(0.60)
]

print("\nFour questions reached:")
print("Should stop:", should_stop(results, 4))
print("Reason:", get_stop_reason(results, 4))