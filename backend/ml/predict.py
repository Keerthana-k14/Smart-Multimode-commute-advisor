import pickle
import os
import numpy as np

_models = {}

def _load(mode: str):
    if mode not in _models:
        path = os.path.join(os.path.dirname(__file__), 'models', f'rf_{mode}.pkl')
        _models[mode] = pickle.load(open(path, 'rb'))
    return _models[mode]

TIME_OF_DAY_MAP = {"morning": 0, "afternoon": 1, "evening": 2}
HOUR_MAP        = {0: 9, 1: 14, 2: 18}
CONGESTION_MAP  = {"low": 0.2, "medium": 0.5, "high": 0.85}

def apply_dynamic_adjustments(times: dict, tod: int, congestion_norm: float, congestion_label: str) -> dict:
    """
    Applies dynamic, pattern-aware adjustments to ML-predicted travel times.
    """
    adjusted = {}
    
    # Mode-specific congestion factors (multipliers for delay)
    # Car: highly affected, Bus: moderately affected, Metro: minimally affected
    CONG_FACTORS = {'car': 0.8, 'bus': 0.5, 'metro': 0.1}
    
    # Peak hour multiplier for road-based modes (Evening peak: 5 PM - 9 PM)
    is_evening_peak = 1 if tod == 2 else 0 # 2 is 'evening' in our map
    TOD_NAMES = {0: "MORNING", 1: "AFTERNOON", 2: "EVENING"}
    
    print(f"\n--- Dynamic Adjustment Debug [{TOD_NAMES.get(tod, 'UNKNOWN')} | {congestion_label.upper()} CONG] ---")
    
    for mode in ['car', 'metro', 'bus']:
        base_time = times[f'{mode}_time']
        
        # 1. Congestion impact (delay is proportional to congestion %)
        cong_delay = base_time * congestion_norm * CONG_FACTORS[mode]
        
        # 2. User Experience (UX) delay - proportional to congestion
        ux_delay = 0
        if mode in ['car', 'bus']:
            ux_delay = base_time * (congestion_norm ** 1.5) * 0.5 
            
        # 3. Peak hour multiplier for road-based modes
        peak_multiplier = 1.0
        if is_evening_peak and mode in ['car', 'bus']:
            peak_multiplier = 1.5 if mode == 'car' else 1.3
            
        # 4. Morning optimization (favoring car/two-wheeler)
        morning_factor = 1.0
        if tod == 0 and mode == 'car': # 0 is 'morning'
            morning_factor = 0.7 
            
        # Compute final adjusted time
        adjusted_time = (base_time + cong_delay + ux_delay) * peak_multiplier * morning_factor
        
        adjusted[f'{mode}_time'] = round(adjusted_time, 1)
        
        print(f"Mode: {mode.upper()}")
        print(f"  Base Time: {base_time} min")
        print(f"  Total Adjustment: {round(adjusted_time - base_time, 1)} min")
        print(f"  FINAL ADJUSTED: {adjusted[f'{mode}_time']} min")
        
    print("----------------------------------------------------------\n")
    return adjusted

def get_prediction(time_of_day: str, day_type: str, congestion: str = "medium", distance_km: float = 10.0) -> dict:
    # Pattern-Aware: Auto-infer congestion level from time_of_day
    # User no longer enters this; it's predicted automatically.
    mapping = {"morning": "low", "afternoon": "medium", "evening": "high"}
    assigned_congestion = mapping.get(time_of_day, "medium")
    
    tod        = TIME_OF_DAY_MAP.get(time_of_day, 1)
    hour       = HOUR_MAP[tod]
    is_weekend = 1 if day_type == "weekend" else 0
    is_peak    = 1 if tod in (0, 2) else 0
    dow        = 6 if is_weekend else 2
    cong_norm  = CONGESTION_MAP.get(assigned_congestion, 0.5)

    X = [[hour, dow, is_peak, is_weekend, tod, cong_norm, distance_km]]

    base_times = {}
    for mode in ['car', 'metro', 'bus']:
        model = _load(mode)
        base_times[f'{mode}_time'] = round(float(model.predict(X)[0]), 1)
    
    # Apply dynamic pattern-aware adjustments
    adjusted_times = apply_dynamic_adjustments(base_times, tod, cong_norm, assigned_congestion)
    
    return adjusted_times