
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/Accidents_Risk_Scored.csv")

print("===== RISK LEVEL VISUALIZATION =====")

counts = df["Risk_Level"].value_counts().reindex(
    ["Low", "Medium", "High", "Very High"],
    fill_value=0
)

print(counts)

counts.plot(kind="bar", figsize=(8, 5))

plt.title("Distribution of Accident Risk Levels")
plt.xlabel("Risk Level")
plt.ylabel("Number of Accidents")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()
