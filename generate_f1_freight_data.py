import random
import math
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ---------------------------
# CONFIGURATION SECTION
# ---------------------------

# Number of records to generate
N = 1000   

# Modes of transport and their probabilities
modes = ["truck", "air", "sea"]
mode_probs = [0.55, 0.35, 0.10]

# Emission factors (kg CO2 per tonne-km)
emission_factors = {
    "truck": 0.15,
    "air": 2.5,
    "sea": 0.02
}

# Formula 1 teams
teams = [
    "Mercedes", "Red Bull", "Ferrari", "McLaren", "Alpine", "Aston Martin",
    "AlphaTauri", "Williams", "Alfa Romeo", "Haas"
]

# Race venues (Name, Latitude, Longitude, Date)
race_venues = [
    ("Bahrain", 26.0325, 50.5106, "2025-03-30"),
    ("Suzuka", 34.8431, 136.5414, "2025-04-20"),
    ("Barcelona", 41.5706, 2.2616, "2025-05-11"),
    ("Monaco", 43.7347, 7.4206, "2025-05-25"),
    ("Silverstone", 52.0733, -1.0146, "2025-07-06"),
    ("Spa", 50.4372, 5.9714, "2025-08-25"),
    ("Monza", 45.6197, 9.2817, "2025-09-07"),
    ("Singapore", 1.2910, 103.8558, "2025-09-21"),
    ("Austin", 30.1328, -97.6411, "2025-10-03"),
    ("Interlagos", -23.7036, -46.6997, "2025-11-15")
]

# ---------------------------
# HELPER FUNCTIONS
# ---------------------------

def haversine(lat1, lon1, lat2, lon2):
    """Compute Haversine distance (in km) between two lat/lon pairs."""
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

def sample_leg():
    """Generate a random freight leg record between two race venues."""
    a, b = random.sample(race_venues, 2)
    name_a, lat_a, lon_a, date_a = a
    name_b, lat_b, lon_b, date_b = b

    mode = random.choices(modes, weights=mode_probs, k=1)[0]
    distance_km = haversine(lat_a, lon_a, lat_b, lon_b)
    if mode == "sea":
        distance_km *= random.uniform(1.2, 1.6)  # longer shipping routes

    weight_tonnes = round(random.uniform(0.5, 20.0), 2)
    load_factor = round(random.uniform(0.6, 1.0), 2)
    factor = emission_factors[mode]

    base_carbon = distance_km * weight_tonnes * factor * load_factor
    noise = base_carbon * random.uniform(-0.07, 0.07)
    if random.random() < 0.03:  # occasional outlier
        noise += base_carbon * random.choice([-0.5, 0.5, 1.0])
    carbon_kg = max(0.0, round(base_carbon + noise, 2))

    dep_date = datetime.strptime(date_a, "%Y-%m-%d") + timedelta(days=random.randint(-3, 1))
    if mode == "air":
        duration_hours = max(1, distance_km / random.uniform(600, 900))
    elif mode == "truck":
        duration_hours = max(4, distance_km / random.uniform(60, 90))
    else:
        duration_hours = max(24, distance_km / random.uniform(20, 40))
    arrival_ts = dep_date + timedelta(hours=duration_hours)

    return {
        "team": random.choice(teams),
        "race_from": name_a,
        "race_to": name_b,
        "mode": mode,
        "distance_km": round(distance_km, 2),
        "weight_tonnes": weight_tonnes,
        "load_factor": load_factor,
        "carbon_kg": carbon_kg,
        "departure_ts": dep_date.isoformat(),
        "arrival_ts": arrival_ts.isoformat(),
        "emission_factor": factor,
        "manual_entry": random.choice([True, False]),
        "notes": random.choice([
            "", "estimated from partial manifest", "sensor glitch - flagged", "validated by DHL data"
        ])
    }

# ---------------------------
# MAIN EXECUTION
# ---------------------------

records = [sample_leg() for _ in range(N)]
df = pd.DataFrame(records)

# Save to CSV
filename = f"synthetic_f1_freight_{N}.csv"
df.to_csv(filename, index=False)
print(f"Generated {N} records and saved to {filename}")
print("\nSample preview:\n", df.head(10))