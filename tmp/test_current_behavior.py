
import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'backend'))
from ml.predict import get_prediction

def test_recommendations():
    scenarios = [
        {"tod": "morning", "dt": "weekday", "cong": "low"},
        {"tod": "afternoon", "dt": "weekday", "cong": "medium"},
        {"tod": "evening", "dt": "weekday", "cong": "high"}
    ]

    for s in scenarios:
        print(f"Scenario: {s}")
        result = get_prediction(s["tod"], s["dt"], s["cong"])
        print(f"Result: {result}")
        best_mode = min(result, key=result.get)
        print(f"Recommended: {best_mode}")
        print("-" * 20)

if __name__ == "__main__":
    test_recommendations()
