import json
import math
import os
from api.routing import get_coordinates, haversine

METRO_SPEED_KMPH = 35.0
WALKING_SPEED_KMPH = 5.0
AUTO_SPEED_KMPH = 20.0
AVERAGE_WAIT_TIME_MINS = 5.0

# Load stations once
STATIONS_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'namma_metro_stations.json')
with open(STATIONS_FILE, 'r') as f:
    METRO_STATIONS = json.load(f)

def get_nearest_station(lat, lon):
    nearest_station = None
    min_dist = float('inf')
    
    for stn in METRO_STATIONS:
        # Note: haversine takes (lon1, lat1, lon2, lat2)
        dist = haversine(lon, lat, stn['lon'], stn['lat'])
        if dist < min_dist:
            min_dist = dist
            nearest_station = stn
            
    return nearest_station, min_dist

def get_metro_commute_time(source_area: str, dest_area: str) -> dict:
    """
    Calculates physical time for a metro journey including multimodal first/last mile.
    """
    if source_area.lower().strip() == dest_area.lower().strip():
        return {"time_mins": 2.0, "is_viable": False, "msg": "Same location"}

    src_coords = get_coordinates(source_area) # returns [lon, lat]
    dst_coords = get_coordinates(dest_area)   # returns [lon, lat]
    
    # 1. Find nearest stations
    src_stn, dist_src = get_nearest_station(src_coords[1], src_coords[0])
    dst_stn, dist_dst = get_nearest_station(dst_coords[1], dst_coords[0])
    
    if src_stn['id'] == dst_stn['id']:
        # They are near the same station, taking metro is illogical
        return {
            "time_mins": 999.0, 
            "is_viable": False, 
            "msg": "Source and destination share the same nearest metro station."
        }
        
    # 2. Calculate times for first/last mile
    # First mile
    if dist_src < 1.5:
        first_mile_time = (dist_src / WALKING_SPEED_KMPH) * 60
        first_mile_mode = "Walk"
    else:
        # Assume Auto/Cab for distance > 1.5km
        first_mile_time = (dist_src / AUTO_SPEED_KMPH) * 60 + 3.0 # +3 min for booking/hailing
        first_mile_mode = "Auto"

    # Last mile
    if dist_dst < 1.5:
        last_mile_time = (dist_dst / WALKING_SPEED_KMPH) * 60
        last_mile_mode = "Walk"
    else:
        last_mile_time = (dist_dst / AUTO_SPEED_KMPH) * 60 + 3.0 
        last_mile_mode = "Auto"
    
    # Metro track distance (approx 1.2 * straight line)
    stn_dist = haversine(src_stn['lon'], src_stn['lat'], dst_stn['lon'], dst_stn['lat']) * 1.2
    
    metro_ride_time = (stn_dist / METRO_SPEED_KMPH) * 60
    
    # Add a penalty for interchange if they are on different lines
    interchange_penalty = 5.0 if src_stn['line'] != dst_stn['line'] and src_stn['line'] != 'Interchange' and dst_stn['line'] != 'Interchange' else 0.0
    
    total_time = first_mile_time + last_mile_time + metro_ride_time + AVERAGE_WAIT_TIME_MINS + interchange_penalty
    
    # Multimodal detail string
    line_info = f"{src_stn['line']} Line" if src_stn['line'] != 'Interchange' else "Metro"
    detail_str = f"{first_mile_mode} ({round(dist_src,1)}km) to {src_stn['name']} → {line_info} to {dst_stn['name']} → {last_mile_mode} ({round(dist_dst,1)}km) to destination."

    # Now always viable as we assume Auto/Cab for longer distances
    return {
        "time_mins": round(total_time, 1),
        "is_viable": True,
        "walk_dist_km": round(dist_src + dist_dst, 1),
        "details": detail_str
    }

if __name__ == "__main__":
    # Test it
    res = get_metro_commute_time("Indiranagar", "Yeshwanthpur")
    print(res)
