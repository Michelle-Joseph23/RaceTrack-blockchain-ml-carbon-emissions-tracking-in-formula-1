import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor
from sklearn.ensemble import IsolationForest

# -------------------------
# 1️. LOAD DATA
# -------------------------
df = pd.read_csv("synthetic_f1_freight_1000.csv")  # your CSV file
print("Data Loaded Successfully! Shape:", df.shape)
print(df.head())

# -------------------------
# 2️. CLEAN + ENCODE DATA
# -------------------------
# Drop text columns not needed for prediction
data = df.copy()
data = data.drop(columns=["race_from", "race_to", "notes", "departure_ts", "arrival_ts"])

# Convert categorical to numerical
data = pd.get_dummies(data, columns=["team", "mode"], drop_first=True)

# Separate features and target
X = data.drop(columns=["carbon_kg"])
y = data["carbon_kg"]

# Split into train-test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale numerical data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# -------------------------
# 3️. TRAIN MODEL (XGBoost)
# -------------------------
model = XGBRegressor(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
)
model.fit(X_train_scaled, y_train)

# -------------------------
# 4️. VALUATE MODEL
# -------------------------
y_pred = model.predict(X_test_scaled)

r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print("\nMetric Scores:")
print(f"R² Score: {r2:.4f}")
print(f"MAE: {mae:.2f} kg CO2")
print(f"RMSE: {rmse:.2f} kg CO2")

# -------------------------
# 5️. FEATURE IMPORTANCE VISUALIZATION
# -------------------------
plt.figure(figsize=(10, 5))
importances = model.feature_importances_
indices = np.argsort(importances)[::-1]
plt.barh(range(len(indices)), importances[indices], align="center")
plt.yticks(range(len(indices)), [X.columns[i] for i in indices])
plt.xlabel("Importance")
plt.title("Feature Importance - XGBoost Model")
plt.gca().invert_yaxis()
plt.show()

# -------------------------
# 6️. ANOMALY DETECTION (Isolation Forest)
# -------------------------
iso = IsolationForest(contamination=0.05, random_state=42)
yhat = iso.fit_predict(X_train_scaled)

# -1 = anomaly, 1 = normal
outliers = X_train[yhat == -1]
print(f"\nDetected {len(outliers)} potential anomalies out of {len(X_train)} records.")

# Add anomaly flag to dataset
data["anomaly_flag"] = iso.fit_predict(scaler.transform(X))
data["predicted_carbon"] = model.predict(scaler.transform(X))

# -------------------------
# 7️. SAVE OUTPUT
# -------------------------
data.to_csv("f1_emission_predictions.csv", index=False)
print("Results saved to f1_emission_predictions.csv")

# -------------------------
# 8️. Visualization
# -------------------------
sns.set(style="whitegrid")
plt.figure(figsize=(7, 7))
sns.scatterplot(x=y_test, y=y_pred, color="royalblue")
plt.xlabel("Actual Emissions (kg CO2)")
plt.ylabel("Predicted Emissions (kg CO2)")
plt.title("Actual vs Predicted Emissions - RaceTrack Model")
plt.show()

# -------------------------
# 9. TEAM & MODE ANALYTICS 
# -------------------------
print("\nPer-Team Emission Analytics")

# Reload original CSV (with text team names) and results
original_df = pd.read_csv("synthetic_f1_freight_1000.csv")
results_df = pd.read_csv("f1_emission_predictions.csv")

# Add original team, mode, and route columns to results
results_df["team"] = original_df["team"]
results_df["mode"] = original_df["mode"]
results_df["race_from"] = original_df["race_from"]
results_df["race_to"] = original_df["race_to"]
results_df["route"] = results_df["race_from"] + " to " + results_df["race_to"]

# Group by team and mode
team_mode_summary = results_df.groupby(["team", "mode"]).agg({
    "carbon_kg": ["mean", "sum", "count"],
    "predicted_carbon": ["mean", "sum"],
    "anomaly_flag": lambda x: (x == -1).sum(),
    "distance_km": "mean",
    "weight_tonnes": "mean"
}).round(2)

# Flatten column names
team_mode_summary.columns = ["avg_actual_kg", "total_actual_kg", "shipment_count", 
                             "avg_predicted_kg", "total_predicted_kg", "anomalies", 
                             "avg_distance_km", "avg_weight_tonnes"]
team_mode_summary = team_mode_summary.reset_index()

print("\n=== TEAM & MODE SUMMARY ===")
print(team_mode_summary)

# Group by route and mode
route_mode_summary = results_df.groupby(["route", "mode"]).agg({
    "carbon_kg": ["mean", "sum", "count"],
    "predicted_carbon": ["mean", "sum"],
    "anomaly_flag": lambda x: (x == -1).sum(),
    "distance_km": "mean",
    "weight_tonnes": "mean"
}).round(2)

# Flatten column names
route_mode_summary.columns = ["avg_actual_kg", "total_actual_kg", "shipment_count",
                             "avg_predicted_kg", "total_predicted_kg", "anomalies",
                             "avg_distance_km", "avg_weight_tonnes"]
route_mode_summary = route_mode_summary.reset_index()

print("\n=== ROUTE & MODE SUMMARY ===")
print(route_mode_summary)

# Save summaries for later blockchain integration
team_mode_summary.to_csv("team_mode_summary.csv", index=False)
route_mode_summary.to_csv("route_mode_summary.csv", index=False)
print("\nSaved team-wise emission summary to team_mode_summary.csv")
print("Saved route-wise emission summary to route_mode_summary.csv")

# Visualizations
plt.figure(figsize=(15, 10))

# Plot 1: Team emissions by mode
plt.subplot(2, 2, 1)
sns.barplot(x="team", y="total_actual_kg", hue="mode", data=team_mode_summary)
plt.title("Total Actual Emissions by Team & Transport Mode")
plt.xticks(rotation=45)
plt.ylabel("CO2 Emissions (kg)")

# Plot 2: Route emissions by mode
plt.subplot(2, 2, 2)
route_top = route_mode_summary.nlargest(15, "total_actual_kg")  # Top 15 routes
sns.barplot(x="route", y="total_actual_kg", hue="mode", data=route_top)
plt.title("Top 15 Routes by Total Emissions")
plt.xticks(rotation=45)
plt.ylabel("CO2 Emissions (kg)")

# Plot 3: Team anomaly count
plt.subplot(2, 2, 3)
team_anomalies = team_mode_summary.groupby("team")["anomalies"].sum().reset_index()
sns.barplot(x="team", y="anomalies", data=team_anomalies)
plt.title("Anomaly Count by Team")
plt.xticks(rotation=45)
plt.ylabel("Number of Anomalies")

# Plot 4: Mode efficiency (emissions per km)
plt.subplot(2, 2, 4)
mode_efficiency = results_df.groupby("mode").agg({
    "carbon_kg": "sum",
    "distance_km": "sum"
}).reset_index()
mode_efficiency["emissions_per_km"] = mode_efficiency["carbon_kg"] / mode_efficiency["distance_km"]
sns.barplot(x="mode", y="emissions_per_km", data=mode_efficiency)
plt.title("Emissions Efficiency by Transport Mode")
plt.ylabel("CO2 Emissions per km (kg/km)")

plt.tight_layout()
plt.show()
