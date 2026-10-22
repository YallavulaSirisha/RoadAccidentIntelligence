import pandas as pd

# Load original dataset
df = pd.read_csv("data/AccidentsBig.csv", low_memory=False)

print("Original shape:", df.shape)

# Remove completely empty rows
df = df.dropna(how="all")

# Remove duplicate rows
df = df.drop_duplicates()

# Remove rows without an Accident ID
df = df.dropna(subset=["Accident_Index"])

# Convert important columns
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
df["Time"] = pd.to_datetime(df["Time"], format="%H:%M", errors="coerce").dt.time

# Save cleaned dataset
df.to_csv("data/Clean_Accidents.csv", index=False)

print("Cleaned shape:", df.shape)
print("Cleaned dataset saved successfully!")