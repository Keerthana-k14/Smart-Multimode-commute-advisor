import random
from datetime import datetime

def get_social_signal(area: str, hour: int) -> str:
    """Simulate Twitter/social traffic sentiment without any API."""
    peak = hour in range(8, 10) or hour in range(17, 20)
    weights = [0.6, 0.3, 0.1] if peak else [0.1, 0.3, 0.6]
    return random.choices(["High", "Medium", "Low"], weights=weights)[0]

def get_realtime_density(area: str) -> float:
    """Simulate real-time traffic density (0.0 to 1.0)."""
    hour = datetime.now().hour
    base = 0.75 if (8 <= hour <= 10 or 17 <= hour <= 20) else 0.3
    noise = random.gauss(0, 0.05)
    return round(max(0.0, min(1.0, base + noise)), 2)

def get_incident_reports(area: str) -> int:
    """Simulate number of active incidents in an area."""
    hour = datetime.now().hour
    peak = 8 <= hour <= 10 or 17 <= hour <= 20
    return random.randint(1, 4) if peak else random.randint(0, 1)

if __name__ == "__main__":
    print("Social signal:", get_social_signal("Koramangala", 18))
    print("Traffic density:", get_realtime_density("Indiranagar"))
    print("Incidents:", get_incident_reports("Whitefield"))