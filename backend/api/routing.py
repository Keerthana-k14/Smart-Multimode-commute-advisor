import requests
import math
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import ORS_API_KEY, ORS_BASE_URL

# Known exact coordinates for Bangalore areas to bypass inaccurate ORS geocoding
KNOWN_LOCATIONS = {
    "indiranagar": [77.6411, 12.9718],
    "whitefield": [77.7499, 12.9698],
    "koramangala": [77.6271, 12.9352],
    "mg road": [77.6015, 12.9730],
    "m.g. road": [77.6015, 12.9730],
    "hebbal": [77.5919, 13.0354],
    "electronic city": [77.6659, 12.8452],
    "jayanagar": [77.5806, 12.9298],
    "jp nagar": [77.5857, 12.9063],
    "yeshwanthpur": [77.5385, 13.0285],
    "bannerghatta road": [77.5960, 12.8800],
    "marathahalli": [77.6980, 12.9569],
    "bellandur": [77.6695, 12.9304],
    "sarjapur road": [77.6830, 12.9150],
    "hsr layout": [77.6385, 12.9121],
    "rajajinagar": [77.5530, 12.9982],
    "malleshwaram": [77.5643, 13.0031],
    "btm layout": [77.6101, 12.9166]
}

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

def get_route_distance(source: str, destination: str) -> float:
    """Gets realistic road distance in km using ORS. Falls back to Haversine."""
    src_coords = get_coordinates(source)
    dst_coords = get_coordinates(destination)
    
    # If same location or very close coords, return a nominal distance
    if source.lower().strip() == destination.lower().strip():
        return 2.0
        
    try:
        url = f"{ORS_BASE_URL}/v2/directions/driving-car"
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
                # distance is in meters -> convert to km
                dist_km = data["routes"][0]["summary"]["distance"] / 1000.0
                return round(dist_km, 1)
    except Exception as e:
        print(f"ORS Routing Error: {e}")
        
    # Haversine Fallback if ORS fails or rate limits
    print("Using HAversine routing fallback...")
    straight_line = haversine(src_coords[0], src_coords[1], dst_coords[0], dst_coords[1])
    
    # Multiply by 1.3 to roughly account for road network detours (Manhattan distance approx)
    road_distance = straight_line * 1.3
    return round(max(2.0, road_distance), 1)

if __name__ == "__main__":
    d = get_route_distance("Bannerghatta Road", "Yeshwanthpur")
    print(f"Distance: {d} km")
