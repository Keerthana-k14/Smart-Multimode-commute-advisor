from fastapi import APIRouter
from pydantic import BaseModel
from ml.predict import get_prediction
from explainer.explain import build_explanation
from api.routing import get_route_distance
import json, os

router = APIRouter()

class PredictRequest(BaseModel):
    area: str          # e.g. "Koramangala"
    road: str          # e.g. "Sony World Junction"
    time_of_day: str   # morning | afternoon | evening
    day_type: str      # weekday | weekend
    congestion: str = "auto"  # low | medium | high (Now auto-handled by backend)

class FeedbackRequest(BaseModel):
    area: str
    road: str
    mode: str
    actual_time: float
    traffic_level: str

@router.post("/predict")
def predict(req: PredictRequest):
    dist_km = get_route_distance(req.area, req.road)
    times    = get_prediction(req.time_of_day, req.day_type, req.congestion, dist_km)
    best_key = min(times, key=times.get)
    best_mode = best_key.replace("_time", "")
    explanation = build_explanation(best_key, times, req.time_of_day, req.congestion)
    return {
        **times,
        "recommended_mode": best_mode,
        "explanation": explanation,
        "area": req.area,
        "road": req.road,
        "distance_km": dist_km
    }

@router.post("/feedback")
def feedback(req: FeedbackRequest):
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'user_feedback.json')
    data = []
    if os.path.exists(path):
        data = json.load(open(path))
    data.append(req.dict())
    json.dump(data, open(path, 'w'), indent=2)
    return {"status": "saved", "total_feedback": len(data)}

@router.get("/routes")
def get_routes():
    # Real areas and roads from our dataset
    return {
        "areas": [
            "Indiranagar", "Whitefield", "Koramangala",
            "MG Road", "Hebbal", "Electronic City"
        ],
        "roads": {
            "Indiranagar":      ["100 Feet Road", "CMH Road"],
            "Whitefield":       ["Marathahalli Bridge", "Whitefield Main Road"],
            "Koramangala":      ["Sony World Junction", "Koramangala 80 Feet Road"],
            "MG Road":          ["MG Road", "Brigade Road"],
            "Hebbal":           ["Hebbal Flyover", "Outer Ring Road"],
            "Electronic City":  ["Electronic City Flyover", "Hosur Road"]
        }
    }