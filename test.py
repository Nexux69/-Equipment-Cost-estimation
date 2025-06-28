# test.py
import pandas as pd
import joblib
from rapidfuzz import process, fuzz
import streamlit as st
from io import BytesIO  # 🔥 Needed for Excel download

# Load saved model data
desc_list, cost_list = joblib.load(r"C:\Users\DELL\Desktop\faiz\cost estimator\cost_model.joblib")

# Define prediction function
def get_best_match_cost(desc, choices, costs, threshold=90):
    match, score, _ = process.extractOne(desc, choices, scorer=fuzz.ratio)
    return costs[choices.index(match)] if score >= threshold else "Not Found"

# Streamlit Web UI
st.title("🧠 Asset Description Cost Predictor")

uploaded_file = st.file_uploader("📤 Upload an Excel file with 'Description' column", type=["xlsx"])

if uploaded_file:
    # Read file
    new_data = pd.read_excel(uploaded_file)
    if "Description" not in new_data.columns:
        st.error("❌ 'Description' column not found in uploaded Excel file.")
    else:
        new_data["Description"] = new_data["Description"].str.strip().str.upper()
        new_data["Predicted Cost"] = new_data["Description"].apply(
            lambda x: get_best_match_cost(x, desc_list, cost_list)
        )

        st.success("✅ Prediction Complete!")
        st.write(new_data)

        # ✅ Fix: Convert to Excel using BytesIO
        output = BytesIO()
        new_data.to_excel(output, index=False, engine='openpyxl')
        output.seek(0)

        st.download_button(
            label="📥 Download Result as Excel",
            data=output,
            file_name="predicted_cost_output.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
