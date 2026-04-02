import pandas as pd
import numpy as np

def load_and_engineer(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    # Parse date and extract time features
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['hour']        = df['Date'].dt.hour.fillna(8).astype(int)
    df['day_of_week'] = df['Date'].dt.dayofweek.fillna(0).astype(int)
    df['is_weekend']  = (df['day_of_week'] >= 5).astype(int)
    df['is_peak']     = df['hour'].apply(
        lambda h: 1 if h in range(8, 10) or h in range(17, 20) else 0
    )
    df['time_of_day_enc'] = df['hour'].apply(
        lambda h: 0 if h < 12 else (1 if h < 17 else 2)
    )

    # Normalize congestion to 0-1
    df['congestion_norm'] = df['Congestion Level'] / 100.0

    # Synthesize a realistic trip distance (between 2 and 35 km)
    np.random.seed(42)
    df['distance_km'] = np.random.uniform(2.0, 35.0, size=len(df)).round(1)

    # Generate travel times per mode based on Distance + Travel Time Index + congestion
    # Assume base free-flow speed is 45 km/h
    base_speed = 45.0 / df['Travel Time Index']
    base_time_minutes = (df['distance_km'] / base_speed) * 60
    
    df['car_travel_time']   = (base_time_minutes * (1 + df['congestion_norm'] * 0.8)).round(1)
    df['metro_travel_time'] = (base_time_minutes * (1 + df['congestion_norm'] * 0.15)).round(1)
    df['bus_travel_time']   = (base_time_minutes * (1 + df['congestion_norm'] * 1.1)).round(1)

    # Route ID from area + road
    df['route_id'] = (
        df['Area Name'].str.lower().str.replace(' ', '_') + '_' +
        df['Road/Intersection Name'].str.lower().str.replace(' ', '_').str.replace('/', '_')
    )

    return df

FEATURES = ['hour', 'day_of_week', 'is_peak', 'is_weekend',
            'time_of_day_enc', 'congestion_norm', 'distance_km']