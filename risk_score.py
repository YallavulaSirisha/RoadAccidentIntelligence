
import pandas as pd

# Load accident data
df = pd.read_csv("data/Accidents_Featured.csv")

# Select required columns and remove missing values
cols = [
    "Accident_Severity",
    "Number_of_Casualties",
    "Speed_limit"
]
df = df.dropna(subset=cols).copy()

# Convert severity to a score: 1 = 3 points, 2 = 2, 3 = 1
df["Severity_Points"] = df["Accident_Severity"].map({
    1: 3,
    2: 2,
    3: 1
})

# Calculate an analytical risk score
df["Risk_Score"] = (
    df["Severity_Points"] * 10
    + df["Number_of_Casualties"].clip(upper=10) * 3
    + df["Speed_limit"].clip(upper=120) / 10
).round(1)

# Classify the scores
def classify(score):
    if score >= 40:
        return "Very High"
    elif score >= 30:
        return "High"
    elif score >= 20:
        return "Medium"
    return "Low"

df["Risk_Level"] = df["Risk_Score"].apply(classify)

# Display results
print("===== ACCIDENT RISK SCORE ANALYSIS =====")
print("\nRisk level counts:")
print(df["Risk_Level"].value_counts())

print("\nTop 10 highest-scoring accidents:")
print(df.nlargest(10, "Risk_Score")[
    ["Accident_Index", "Accident_Severity",
     "Number_of_Casualties", "Speed_limit",
     "Risk_Score", "Risk_Level"]
])

# Save results
df.to_csv("data/Accidents_Risk_Scored.csv", index=False)

print("\nRisk analysis completed!")
print("Saved to: data/Accidents_Risk_Scored.csv")
