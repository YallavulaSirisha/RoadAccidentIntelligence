
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/Accidents_Featured.csv")

df = df.dropna(subset=[
    "Number_of_Vehicles",
    "Number_of_Casualties"
])

print("===== VEHICLES VS CASUALTIES =====")

summary = df.groupby("Number_of_Vehicles")[
    "Number_of_Casualties"
].agg(["count", "mean", "sum"])

print("\nVehicles vs Casualties:")
print(summary)

# Average casualties by number of vehicles
average = summary["mean"]

average.plot(kind="bar", figsize=(9, 5))

plt.title("Number of Vehicles vs Average Casualties")
plt.xlabel("Number of Vehicles")
plt.ylabel("Average Number of Casualties")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

