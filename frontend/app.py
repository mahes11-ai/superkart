import json
import requests
import streamlit as st

st.set_page_config(page_title="SuperKart Sales Forecast", layout="wide")
st.title("SuperKart Sales Forecast")
st.caption("Predict future sales revenue for a product-store combination")

backend_url = "http://superkart-backend:7860"

with st.form("forecast_form"):
    col1, col2 = st.columns(2)

    with col1:
        product_weight = st.number_input("Product Weight", min_value=0.0, value=12.66, step=0.01)
        product_sugar = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
        product_allocated_area = st.number_input("Product Allocated Area", min_value=0.0, value=0.027, step=0.001)
        product_mrp = st.number_input("Product MRP", min_value=0.0, value=117.08, step=0.01)
        product_type = st.selectbox("Product Type", ["Perishables", "Non Perishables"])

    with col2:
        store_size = st.selectbox("Store Size", ["Small", "Medium", "High"])
        city_type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
        store_type = st.selectbox("Store Type", ["Departmental Store", "Supermarket Type1", "Supermarket Type2", "Food Mart"])
        product_id_char = st.text_input("Product ID Prefix", value="FD").upper()
        store_age_years = st.number_input("Store Age (Years)", min_value=0, value=16, step=1)

    submitted = st.form_submit_button("Predict Sales")

if submitted:
    payload = {
        "Product_Weight": product_weight,
        "Product_Sugar_Content": product_sugar,
        "Product_Allocated_Area": product_allocated_area,
        "Product_MRP": product_mrp,
        "Store_Size": store_size,
        "Store_Location_City_Type": city_type,
        "Store_Type": store_type,
        "Product_Id_char": product_id_char,
        "Store_Age_Years": int(store_age_years),
        "Product_Type_Category": product_type,
    }

    response = requests.post(f"{backend_url}/v1/predict", json=payload, timeout=30)
    if response.ok:
        prediction = response.json()["predicted_sales"]
        st.success(f"Estimated sales: ${prediction:,.2f}")
    else:
        st.error(f"Prediction failed: {response.text}")
