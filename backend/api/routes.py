from fastapi import APIRouter
from pydantic import BaseModel
from ml.predict import get_prediction
from explainer.explain import build_explanation
from api.routing import get_route_distance, get_route_time_and_distance, get_all_location_names
import json, os

router = APIRouter()

class PredictRequest(BaseModel):
    area: str          # e.g. "Koramangala"
    road: str          # e.g. "Sony World Junction"
    time_of_day: str   # morning | afternoon | evening
    day_type: str      # weekday | weekend
    congestion: str = "auto"  # low | medium | high (Now auto-handled by backend)

class DistanceRequest(BaseModel):
    source: str
    destination: str
    time_of_day: str = "default"  # morning | afternoon | evening | default

class FeedbackRequest(BaseModel):
    area: str
    road: str
    mode: str
    actual_time: float
    traffic_level: str

@router.post("/predict")
def predict(req: PredictRequest):
    # 1. Get physical distance and calibrated engine times (Source of Truth)
    distance_info = get_route_time_and_distance(req.area, req.road, req.time_of_day)
    dist_km = distance_info["distance_km"]

    # 2. Get ML-based patterns (for background logic/explanation)
    ml_times = get_prediction(req.time_of_day, req.day_type, req.congestion, dist_km)
    
    # Synchronize: Use the physics engine times for the UI tiles to ensure NO VARIATION
    # The Physics engine is already calibrated to match Google Maps targets.
    sync_times = {
        "car_time":   distance_info["modes"]["car"]["time_mins"],
        "bike_time":  distance_info["modes"]["bike"]["time_mins"],
        "bus_time":   distance_info["modes"]["bus"]["time_mins"],
        "metro_time": distance_info["modes"]["metro"]["time_mins"]
    }

    best_key = min(sync_times, key=sync_times.get)
    best_mode = best_key.replace("_time", "")
    
    # Pass sync_times to explainer for consistency
    explanation = build_explanation(best_key, sync_times, req.time_of_day, req.congestion)

    return {
        **sync_times,
        "recommended_mode": best_mode,
        "explanation": explanation,
        "area": req.area,
        "road": req.road,
        "distance_km": dist_km,
        "distance_info": distance_info
    }


@router.post("/distance")
def get_distance(req: DistanceRequest):
    """Returns distance and time breakdown for all transport modes between two Bengaluru places."""
    result = get_route_time_and_distance(req.source, req.destination, req.time_of_day)
    return result


@router.post("/feedback")
def feedback(req: FeedbackRequest):
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'user_feedback.json')
    data = []
    if os.path.exists(path):
        data = json.load(open(path))
    data.append(req.dict())
    json.dump(data, open(path, 'w'), indent=2)
    return {"status": "saved", "total_feedback": len(data)}

@router.get("/config/map")
def get_map_config():
    from config import OLA_API_KEY
    return {"apiKey": OLA_API_KEY}

@router.get("/routes")
def get_routes():
    # Dynamic: return all known Bengaluru locations
    all_locations = get_all_location_names()
    return {
        "locations": all_locations,
        # Legacy format for backward compatibility
        "areas": all_locations[:20],
        "roads": {}
    }