import os

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
DATA_DIR  = os.path.join(BASE_DIR, "data")
RAW_CSV   = os.path.join(DATA_DIR, "raw", "Banglore_traffic_Dataset.csv")
PROCESSED = os.path.join(DATA_DIR, "processed", "features.csv")
MODELS_DIR = os.path.join(BASE_DIR, "ml", "models")
FEEDBACK_FILE = os.path.join(DATA_DIR, "user_feedback.json")

API_TITLE   = "Smart Commute Advisor"
API_VERSION = "1.0.0"

# OpenRouteService Configuration
# Get your API key from https://openrouteservice.org/
ORS_API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjE3YjAzYWNiMjRjNDQwYTU4N2M2ZmIzMzRkMzVlMDU4IiwiaCI6Im11cm11cjY0In0="
ORS_BASE_URL = "https://api.openrouteservice.org"

# Ola Maps Configuration
OLA_PROJECT_ID = "041d9adb-1d8d-4304-9a7b-373fdc999f78"
OLA_API_KEY = "nlDvre2y4A2hqUQCLTypfdsG2FSofriUProAtSD0"
OLA_CLIENT_ID = "041d9adb-1d8d-4304-9a7b-373fdc999f78"
OLA_CLIENT_SECRET = "d17baacd9c5e40de92f79ec8b1f44906"
OLA_BASE_URL = "https://api.olamaps.io"