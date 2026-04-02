from pydantic import BaseModel
from typing import Optional

class PredictRequest(BaseModel):
    area: str
    road: str
    time_of_day: str    # morning | afternoon | evening
    day_type: str       # weekday | weekend
    congestion: str     # low | medium | high

class PredictResponse(BaseModel):
    area: str
    road: str
    recommended_mode: str
    car_time: float
    metro_time: float
    bus_time: float
    explanation: str

class FeedbackRequest(BaseModel):
    area: str
    road: str
    mode: str
    actual_time: float
    traffic_level: str

class FeedbackResponse(BaseModel):
    status: str
    total_feedback: int