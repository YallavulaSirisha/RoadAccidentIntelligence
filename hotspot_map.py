
import pandas as pd
import folium
from folium.plugins import HeatMap

# Load accident data
df = pd.read_csv("data/Accidents_Featured.csv")

# Convert coordinates to numbers
df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")

# Remove missing and invalid coordinates
df = df.dropna(subset=["latitude", "longitude"])
df = df[
    df["latitude"].between(-90, 90) &
    df["longitude"].between(-180, 180)
]

print("===== ACCIDENT HOTSPOT MAP =====")
print("Valid accident locations:", len(df))

if df.empty:
    print("No valid accident coordinates found.")
else:
    # Center map on the accident locations
    center = [df["latitude"].mean(), df["longitude"].mean()]

    accident_map = folium.Map(
        location=center,
        zoom_start=6
    )

    # Use a sample for a faster map
    points = df[["latitude", "longitude"]]
    if len(points) > 10000:
        points = points.sample(10000, random_state=42)

    # Add accident hotspot layer
    HeatMap(points.values.tolist(), radius=10).add_to(accident_map)

    # Save map
    accident_map.save("outputs/accident_hotspot_map.html")

    print("Map created successfully!")
    print("Saved to: outputs/accident_hotspot_map.html")
