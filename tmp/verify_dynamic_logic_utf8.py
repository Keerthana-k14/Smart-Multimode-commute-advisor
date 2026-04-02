
import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'backend'))
from ml.predict import get_prediction

def verify_dynamic_logic():
    scenarios = [
        {
            "name": "TEST CASE 1: Morning + Low Congestion",
            "params": {"time_of_day": "morning", "day_type": "weekday", "congestion": "low"}
        },
        {
            "name": "TEST CASE 2: Afternoon + Medium Congestion",
            "params": {"time_of_day": "afternoon", "day_type": "weekday", "congestion": "medium"}
        },
        {
            "name": "TEST CASE 3: Evening + High Congestion",
            "params": {"time_of_day": "evening", "day_type": "weekday", "congestion": "high"}
        }
    ]

    with open('tmp/verification_results.txt', 'w', encoding='utf-8') as f:
        # Redirect stdout to file
        old_stdout = sys.stdout
        sys.stdout = f
        
        try:
            for s in scenarios:
                print("="*60)
                print(f"{s['name']}")
                print(f"Input: {s['params']}")
                
                # This will trigger the print statements in apply_dynamic_adjustments
                result = get_prediction(**s['params'])
                
                best_mode = min(result, key=result.get)
                print(f"Final Outcome -> Recommended Mode: {best_mode.replace('_time', '').upper()}")
                print(f"Final Times -> {result}")
                print("="*60 + "\n")
        finally:
            sys.stdout = old_stdout

if __name__ == "__main__":
    verify_dynamic_logic()
