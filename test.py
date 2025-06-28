import pandas as pd
import streamlit as st
import joblib

# Load the saved model
desc_list, cost_list = joblib.load("cost_model.joblib")

# Page title
st.title("🧮 Equipment Cost Estimator")
st.markdown("Upload an Excel file with a 'Description' column to predict equipment cost.")

# Upload input Excel file
uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

# Predict cost
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    if "Description" not in df.columns:
        st.error("The uploaded Excel file must have a 'Description' column.")
    else:
        from rapidfuzz import process

        def fuzzy_predict(description):
            match, score, index = process.extractOne(description, desc_list)
            return cost_list[index]

        # Apply prediction
        df["Predicted Cost"] = df["Description"].apply(fuzzy_predict)

        # Round the results to 2 decimal places
        df["Predicted Cost"] = df["Predicted Cost"].round(2)

        # Display result
        st.success("✅ Prediction Complete!")
        st.dataframe(df)

        # Download button
        st.download_button(
            label="📥 Download Results as Excel",
            data=df.to_excel(index=False, engine='openpyxl'),
            file_name="predicted_costs.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
