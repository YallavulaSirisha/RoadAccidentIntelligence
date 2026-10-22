import pandas as pd

# Load cleaned data
df = pd.read_csv("data/Clean_Accidents.csv", low_memory=False)

# Convert date and time
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Time"] = pd.to_datetime(df["Time"], format="%H:%M:%S", errors="coerce")

# Create new features
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["Month_Name"] = df["Date"].dt.month_name()
df["Hour"] = df["Time"].dt.hour
df["Day_Name"] = df["Date"].dt.day_name()

# Weekend
df["Weekend"] = df["Date"].dt.dayofweek >= 5

# Time period
def get_period(hour):
    if pd.isna(hour):
        return "Unknown"
    elif 5 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 17:
        return "Afternoon"
    elif 17 <= hour < 21:
        return "Evening"
    else:
        return "Night"

df["Time_Period"] = df["Hour"].apply(get_period)

# Save feature-engineered dataset
df.to_csv("data/Accidents_Featured.csv", index=False)

print("Feature engineering completed!")
print("New shape:", df.shape)

print("\nNew columns:")
print([
    "Year",
    "Month",
    "Month_Name",
    "Hour",
    "Day_Name",
    "Weekend",
    "Time_Period"
])