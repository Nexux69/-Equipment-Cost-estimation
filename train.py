# train.py
import pandas as pd
import joblib

# Load dataset
df = pd.read_excel(r"C:\Users\DELL\Desktop\faiz\cost estimator\cleaned_asset_description_cost.xlsx")
df = df[1:]
df.columns = ["Description", "Cost"]
df["Description"] = df["Description"].str.strip().str.upper()
df.dropna(inplace=True)

# Save descriptions and costs as lists
desc_list = df["Description"].tolist()
cost_list = df["Cost"].tolist()

# Save them using joblib
joblib.dump((desc_list, cost_list), "cost_model.joblib")
print("Model saved as cost_model.joblib")
