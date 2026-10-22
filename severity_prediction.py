
import pandas as pd
import matplotlib.pyplot as plt
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, ConfusionMatrixDisplay, accuracy_score

df = pd.read_csv("data/Accidents_Featured.csv")

features = [
    "Number_of_Vehicles", "Speed_limit", "Road_Type",
    "Weather_Conditions", "Light_Conditions",
    "Road_Surface_Conditions", "Urban_or_Rural_Area",
    "Junction_Detail", "Junction_Control", "Day_of_Week"
]

df = df[features + ["Accident_Severity"]].dropna()

X = pd.get_dummies(df[features])
y = df["Accident_Severity"].astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = RandomForestClassifier(
    n_estimators=200,
    class_weight="balanced",
    min_samples_leaf=3,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)
predictions = model.predict(X_test)

print("===== IMPROVED ACCIDENT SEVERITY PREDICTION =====")
print("Accuracy:", round(accuracy_score(y_test, predictions) * 100, 2), "%")
print(classification_report(y_test, predictions, zero_division=0))

ConfusionMatrixDisplay.from_predictions(y_test, predictions)
plt.title("Improved Accident Severity Prediction")
plt.tight_layout()
plt.show()

joblib.dump(
    {"model": model, "columns": X.columns.tolist()},
    "models/severity_model.pkl"
)

print("Improved model saved successfully!")

