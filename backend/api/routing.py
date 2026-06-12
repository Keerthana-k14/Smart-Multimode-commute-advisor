import requests
import math
import sys
import os
import time
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import ORS_API_KEY, ORS_BASE_URL, OLA_PROJECT_ID, OLA_API_KEY, OLA_CLIENT_ID, OLA_CLIENT_SECRET, OLA_BASE_URL

# Load metro stations
METRO_STATIONS_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'namma_metro_stations.json')
with open(METRO_STATIONS_FILE, 'r') as f:
    METRO_STATIONS = json.load(f)

METRO_STATION_NAMES = {stn['id'].lower(): stn for stn in METRO_STATIONS}
METRO_STATION_NAMES.update({stn['name'].lower(): stn for stn in METRO_STATIONS})

# Ola Maps access token cache
_ola_token = None
_token_expiry = 0

def _get_ola_token():
    global _ola_token, _token_expiry
    if _ola_token and time.time() < _token_expiry:
        return _ola_token
    try:
        url = "https://account.olamaps.io/realms/olamaps/protocol/openid-connect/token"
        data = {
            "client_id": OLA_CLIENT_ID,
            "client_secret": OLA_CLIENT_SECRET,
            "grant_type": "client_credentials"
        }
        res = requests.post(url, data=data, timeout=10)
        if res.status_code == 200:
            token_data = res.json()
            _ola_token = token_data["access_token"]
            expires_in = token_data.get("expires_in", 3600)  # default 1 hour
            _token_expiry = time.time() + expires_in - 60  # 1 min buffer
            return _ola_token
    except Exception as e:
        print(f"Ola token error: {e}")
    return None

# ────────────────────────────────────────────────────────────────────────────
# 50+ Bengaluru locations — accurate [lon, lat] coordinates
# ────────────────────────────────────────────────────────────────────────────
KNOWN_LOCATIONS = {
    # Central Bengaluru
    "mg road":              [77.6015, 12.9730],
    "m.g. road":            [77.6015, 12.9730],
    "brigade road":         [77.6070, 12.9716],
    "majestic":             [77.5728, 12.9757],
    "shivajinagar":         [77.5945, 12.9857],
    "ulsoor":               [77.6206, 12.9812],
    "cubbon park":          [77.5918, 12.9763],
    "richmond town":        [77.5993, 12.9614],

    # East Bengaluru
    "indiranagar":          [77.6411, 12.9718],
    "domlur":               [77.6370, 12.9610],
    "koramangala":          [77.6271, 12.9352],
    "hsr layout":           [77.6385, 12.9121],
    "btm layout":           [77.6101, 12.9166],
    "bellandur":            [77.6695, 12.9304],
    "sarjapur road":        [77.6830, 12.9150],
    "marathahalli":         [77.6980, 12.9569],
    "whitefield":           [77.7499, 12.9698],
    "hal":                  [77.6589, 12.9591],
    "old airport road":     [77.6472, 12.9635],
    "varthur":              [77.7400, 12.9400],
    "kadugodi":             [77.7612, 12.9961],
    "kr puram":             [77.7030, 12.9980],
    "mahadevapura":         [77.7150, 12.9910],

    # South Bengaluru
    "jayanagar":            [77.5806, 12.9298],
    "jp nagar":             [77.5857, 12.9063],
    "bannerghatta road":    [77.5960, 12.8800],
    "electronic city":      [77.6659, 12.8452],
    "silk board":           [77.6238, 12.9177],
    "bommanahalli":         [77.6183, 12.9000],
    "basavanagudi":         [77.5747, 12.9430],
    "banashankari":         [77.5630, 12.9250],
    "kumaraswamy layout":   [77.5650, 12.9100],
    "kanakapura road":      [77.5700, 12.8900],
    "uttarahalli":          [77.5470, 12.9020],
    "arekere":              [77.6020, 12.8870],
    "wilson garden":        [77.5960, 12.9460],
    "lalbagh":              [77.5855, 12.9507],

    # North Bengaluru
    "hebbal":               [77.5919, 13.0354],
    "yeshwanthpur":         [77.5385, 13.0285],
    "rajajinagar":          [77.5530, 12.9982],
    "malleshwaram":         [77.5643, 13.0031],
    "sadashivanagar":       [77.5800, 13.0090],
    "yelahanka":            [77.5970, 13.1000],
    "thanisandra":          [77.6360, 13.0590],
    "nagawara":             [77.6160, 13.0410],
    "rt nagar":             [77.5940, 13.0210],
    "banaswadi":            [77.6470, 13.0110],
    "hennur":               [77.6400, 13.0380],
    "kalyan nagar":         [77.6360, 13.0220],

    # West Bengaluru
    "vijayanagar":          [77.5350, 12.9700],
    "basaveshwaranagar":    [77.5380, 12.9870],
    "nagarbhavi":           [77.5080, 12.9600],
    "kengeri":              [77.4870, 12.9130],
    "peenya":               [77.5210, 13.0300],
    "magadi road":          [77.5420, 12.9660],
    "mysore road":          [77.5300, 12.9500],
    "rr nagar":             [77.5100, 12.9350],
    "nayandahalli":         [77.5190, 12.9520],

    # Outer / IT Corridors
    "hosur road":           [77.6350, 12.8900],
    "tumkur road":          [77.5400, 13.0500],
    "outer ring road":      [77.6800, 12.9350],
    "devanahalli":          [77.7100, 13.2500],
    "kempegowda airport":   [77.7068, 13.1989],
    "hoskote":              [77.7980, 13.0710],
    "anekal":               [77.6940, 12.7100],
    "begur":                [77.6290, 12.8760],
    "hulimavu":             [77.5990, 12.8820],
    "jp nagar 6th phase":   [77.5720, 12.8880],
    "gottigere":            [77.5830, 12.8700],
    "konanakunte":          [77.5680, 12.8830],
}

# ────────────────────────────────────────────────────────────────────────────
# Bengaluru average speed models (km/h) per mode and time-of-day
# Calibrated to match Google Maps (e.g. Koramangala-Whitefield ~17km: Car ~55m, Bike ~44m)
# ────────────────────────────────────────────────────────────────────────────
SPEED_PROFILES = {
    "car":   {"morning": 20, "afternoon": 30, "evening": 19, "default": 24},
    "bike":  {"morning": 25, "afternoon": 35, "evening": 24, "default": 28},
    "bus":   {"morning": 14, "afternoon": 20, "evening": 12, "default": 16},
    "metro": {"morning": 35, "afternoon": 35, "evening": 35, "default": 35},
}

# ────────────────────────────────────────────────────────────────────────────
# In-memory cache with TTL (5 minutes)
# ────────────────────────────────────────────────────────────────────────────
_route_cache = {}
CACHE_TTL = 300  # seconds

def _cache_key(src, dst, profile="driving-car"):
    return f"{src.lower().strip()}|{dst.lower().strip()}|{profile}"

def _get_cached(key):
    if key in _route_cache:
        entry = _route_cache[key]
        if time.time() - entry["ts"] < CACHE_TTL:
            return entry["data"]
        del _route_cache[key]
    return None

def _set_cache(key, data):
    _route_cache[key] = {"data": data, "ts": time.time()}


def haversine(lon1, lat1, lon2, lat2):
    """Calculates the great circle distance between two points in km."""
    R = 6371.0 # Earth radius in km
    dlon = math.radians(lon2 - lon1)
    dlat = math.radians(lat2 - lat1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

def get_coordinates(location: str):
    """Fetch exact coordinates for known areas, bypassing ORS Geocoder for reliability."""
    loc_key = location.lower().replace(" bridge", "").replace(" junction", "").replace(" flyover", "").strip()
    
    # 1. Exact Match
    if loc_key in KNOWN_LOCATIONS:
        return KNOWN_LOCATIONS[loc_key]
        
    # 2. Substring Match
    for key, coords in KNOWN_LOCATIONS.items():
        if key in loc_key or loc_key in key:
            return coords
            
    # 3. Fallback ORS Geocoding
    try:
        query = f"{location}, Bangalore, India"
        url = f"{ORS_BASE_URL}/geocode/search"
        params = {"api_key": ORS_API_KEY, "text": query, "size": 1}
        res = requests.get(url, params=params, timeout=5)
        if res.status_code == 200:
            data = res.json()
            if data and "features" in data and len(data["features"]) > 0:
                return data["features"][0]["geometry"]["coordinates"] # [lon, lat]
    except Exception as e:
        print(f"Geocoding Error for {location}: {e}")

    # 4. Absolute fallback (Central Bangalore)
    print(f"Fallback missing for {location}, returning central Bangalore.")
    return [77.5946, 12.9716]


def _ola_route(src_coords, dst_coords, mode="driving"):
    """Call Ola Maps directions API. Returns (distance_km, time_mins) or None."""
    token = _get_ola_token()
    if not token:
        return None
    try:
        url = f"{OLA_BASE_URL}/routing/v1/directions"
        headers = {"Authorization": f"Bearer {token}"}
        params = {
            "origin": f"{src_coords[1]},{src_coords[0]}",  # lat,lon
            "destination": f"{dst_coords[1]},{dst_coords[0]}",
            "mode": mode,
            "alternatives": "false"
        }
        res = requests.get(url, headers=headers, params=params, timeout=10)
        if res.status_code == 200:
            data = res.json()
            if "routes" in data and len(data["routes"]) > 0:
                route = data["routes"][0]
                dist_m = route["distance"]
                time_s = route["duration"]
                dist_km = round(dist_m / 1000.0, 1)
                time_mins = round(time_s / 60.0, 1)
                return dist_km, time_mins
    except Exception as e:
        print(f"Ola routing error ({mode}): {e}")
    return None


def _ors_route(src_coords, dst_coords, profile="driving-car"):
    """Call ORS directions API for a given profile. Returns (distance_km, time_mins) or None."""
    try:
        url = f"{ORS_BASE_URL}/v2/directions/{profile}"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": ORS_API_KEY
        }
        payload = {
            "coordinates": [src_coords, dst_coords]
        }
        res = requests.post(url, json=payload, headers=headers, timeout=5)
        if res.status_code == 200:
            data = res.json()
            if "routes" in data and len(data["routes"]) > 0:
                summary = data["routes"][0]["summary"]
                dist_km = round(summary["distance"] / 1000.0, 1)
                time_mins = round(summary["duration"] / 60.0, 1)
                return dist_km, time_mins
    except Exception as e:
        print(f"ORS Routing Error ({profile}): {e}")
    return None


def get_route_distance(source: str, destination: str) -> float:
    """Gets realistic road distance in km using Ola Maps. Falls back to Haversine."""
    src_coords = get_coordinates(source)
    dst_coords = get_coordinates(destination)
    
    # If same location or very close coords, return a nominal distance
    if source.lower().strip() == destination.lower().strip():
        return 2.0

    # Check cache
    ck = _cache_key(source, destination, "driving")
    cached = _get_cached(ck)
    if cached:
        return cached["distance_km"]

    result = _ola_route(src_coords, dst_coords, "driving")
    if result:
        dist_km, time_mins = result
        _set_cache(ck, {"distance_km": dist_km, "time_mins": time_mins})
        return dist_km
        
    # Haversine Fallback if Ola fails
    print("Using Haversine routing fallback...")
    straight_line = haversine(src_coords[0], src_coords[1], dst_coords[0], dst_coords[1])
    
    # Multiply by 1.3 to roughly account for road network detours (Manhattan distance approx)
    road_distance = straight_line * 1.3
    return round(max(2.0, road_distance), 1)


def is_metro_station(location: str) -> bool:
    """Check if location is a known metro station."""
    loc_key = location.lower().strip()
    return loc_key in METRO_STATION_NAMES


def get_metro_route_time(source: str, destination: str) -> dict:
    """Get metro time if both are stations, else not viable."""
    if not is_metro_station(source) or not is_metro_station(destination):
        return {"time_mins": 999.0, "distance_km": 0.0, "details": "Not metro stations", "is_viable": False}
    
    src_stn = METRO_STATION_NAMES[source.lower().strip()]
    dst_stn = METRO_STATION_NAMES[destination.lower().strip()]
    
    if src_stn['id'] == dst_stn['id']:
        return {"time_mins": 2.0, "distance_km": 0.0, "details": "Same station", "is_viable": False}
    
    # Calculate distance and time
    dist = haversine(src_stn['lon'], src_stn['lat'], dst_stn['lon'], dst_stn['lat']) * 1.2  # approx track distance
    time_mins = (dist / 35.0) * 60 + 5  # speed + wait
    
    # Interchange penalty
    interchange = 5.0 if src_stn['line'] != dst_stn['line'] else 0.0
    time_mins += interchange
    
    return {
        "time_mins": round(time_mins, 1),
        "distance_km": round(dist, 1),
        "details": f"Direct metro from {src_stn['name']} to {dst_stn['name']}",
        "is_viable": True
    }


def get_route_time_and_distance(source: str, destination: str, time_of_day: str = "default") -> dict:
    """
    Returns distance_km and travel_time_mins for each transport mode (car, bike, bus, metro).
    Uses Ola Maps for car/bike/bus road distance.
    Metro uses dedicated metro_routing module with multimodal support.
    
    Returns:
        {
            "source": ..., "destination": ...,
            "distance_km": float,    # road distance
            "source_coords": [lon, lat],
            "dest_coords": [lon, lat],
            "modes": {
                "car":   {"time_mins": float, "distance_km": float},
                "bike":  {"time_mins": float, "distance_km": float},
                "bus":   {"time_mins": float, "distance_km": float},
                "metro": {"time_mins": float, "distance_km": float, "details": str, "is_viable": bool}
            },
            "recommended": str
        }
    """
    if source.lower().strip() == destination.lower().strip():
        return {
            "source": source,
            "destination": destination,
            "distance_km": 0.0,
            "source_coords": get_coordinates(source),
            "dest_coords": get_coordinates(destination),
            "modes": {
                "car":   {"time_mins": 0.0, "distance_km": 0.0},
                "bike":  {"time_mins": 0.0, "distance_km": 0.0},
                "bus":   {"time_mins": 0.0, "distance_km": 0.0},
                "metro": {"time_mins": 0.0, "distance_km": 0.0, "details": "Same location", "is_viable": False},
            },
            "recommended": "car"
        }

    src_coords = get_coordinates(source)
    dst_coords = get_coordinates(destination)

    # ── 1. Get road distance + car time from Ola (or cache) ──────────────
    ck = _cache_key(source, destination, "driving")
    cached = _get_cached(ck)

    if cached:
        road_dist = cached["distance_km"]
        car_time_ola = cached.get("time_mins")
    else:
        ola_result = _ola_route(src_coords, dst_coords, "driving")
        if ola_result:
            road_dist, car_time_ola = ola_result
            _set_cache(ck, {"distance_km": road_dist, "time_mins": car_time_ola})
        else:
            # Haversine fallback
            straight_line = haversine(src_coords[0], src_coords[1], dst_coords[0], dst_coords[1])
            road_dist = round(max(2.0, straight_line * 1.3), 1)
            car_time_ola = None

    # ── 2. Compute per-mode travel times ─────────────────────────────────
    tod = time_of_day if time_of_day in ("morning", "afternoon", "evening") else "default"

    # Car time: prefer real-time Ola estimate, else speed-based
    if car_time_ola is not None:
        # User goal: Koramangala-Whitefield (~17km) Car ~55m
        # If Ola gives something else, we might need a slight "calibrator" factor
        # based on Bangalore's unique peak traffic density.
        car_time = car_time_ola 
    else:
        car_speed = SPEED_PROFILES["car"][tod]
        car_time = round((road_dist / car_speed) * 60, 1)

    # Bike time: Generally faster in traffic than a car
    # User goal: Koramangala-Whitefield (~17km) Bike ~44m
    if car_time_ola is not None:
        # Bike is usually 20-30% faster than car in heavy traffic
        bike_time = round(car_time * 0.8, 1)
    else:
        bike_speed = SPEED_PROFILES["bike"][tod]
        bike_time = round((road_dist / bike_speed) * 60, 1)

    # Bus time: car time + wait + stops
    if car_time_ola is not None:
        bus_time = round(car_time * 1.4 + 5, 1)
    else:
        bus_speed = SPEED_PROFILES["bus"][tod]
        bus_time = round((road_dist / bus_speed) * 60 + 8, 1)

    # Metro time: use dedicated metro routing module (now multimodal)
    try:
        from api.metro_routing import get_metro_commute_time
        metro_result = get_metro_commute_time(source, destination)
        metro_time = metro_result["time_mins"]
        metro_viable = metro_result["is_viable"]
        metro_details = metro_result["details"]
    except Exception as e:
        print(f"Metro routing error: {e}")
        metro_time = 999.0
        metro_viable = False
        metro_details = "Metro route unavailable"

    # ── 3. Determine recommendation ──────────────────────────────────────
    candidates = {"car": car_time, "bike": bike_time, "bus": bus_time}
    if metro_viable and metro_time < 999:
        candidates["metro"] = metro_time

    recommended = min(candidates, key=candidates.get)

    return {
        "source": source,
        "destination": destination,
        "distance_km": road_dist,
        "source_coords": src_coords,
        "dest_coords": dst_coords,
        "modes": {
            "car":   {"time_mins": car_time,   "distance_km": road_dist},
            "bike":  {"time_mins": bike_time,  "distance_km": road_dist},
            "bus":   {"time_mins": bus_time,    "distance_km": round(road_dist * 1.05, 1)}, 
            "metro": {
                "time_mins": metro_time if metro_viable else 999.0,
                "distance_km": round(road_dist * 0.9, 1),
                "details": metro_details,
                "is_viable": metro_viable
            },
        },
        "recommended": recommended
    }


def get_all_location_names() -> list:
    """Returns all known Bengaluru location names and metro stations, title-cased."""
    seen = set()
    names = []
    for key in KNOWN_LOCATIONS:
        # Deduplicate aliases (e.g. "mg road" and "m.g. road")
        display = key.title()
        # Normalize known aliases
        if display in seen:
            continue
        seen.add(display)
        names.append(display)
    
    # Add metro stations
    for stn in METRO_STATIONS:
        display = stn['name']
        if display not in seen:
            seen.add(display)
            names.append(display)
    
    return sorted(names)


if __name__ == "__main__":
    d = get_route_distance("Bannerghatta Road", "Yeshwanthpur")
    print(f"Distance: {d} km")
    
    print("\n--- Full time & distance ---")
    result = get_route_time_and_distance("Koramangala", "Whitefield", "evening")
    for k, v in result.items():
        print(f"  {k}: {v}")
