from flask import Flask, request, jsonify
import joblib
import os
import pandas as pd

app = Flask(__name__)
MODEL_PATH = os.path.join("backend_files", "superkart_model.joblib")
model = joblib.load(MODEL_PATH)

def prepare_input(payload):
    record = {
        "Product_Weight": float(payload["Product_Weight"]),
        "Product_Sugar_Content": payload["Product_Sugar_Content"],
        "Product_Allocated_Area": float(payload["Product_Allocated_Area"]),
        "Product_Type_Category": payload.get("Product_Type_Category", payload.get("Product_Type")),
        "Product_MRP": float(payload["Product_MRP"]),
        "Store_Size": payload["Store_Size"],
        "Store_Location_City_Type": payload["Store_Location_City_Type"],
        "Store_Type": payload["Store_Type"],
        "Product_Id_char": payload["Product_Id_char"],
        "Store_Age_Years": int(payload["Store_Age_Years"]),
    }
    return pd.DataFrame([record])

@app.route("/v1/predict", methods=["POST"])
def predict():
    payload = request.get_json(force=True)
    features = prepare_input(payload)
    prediction = float(model.predict(features)[0])
    return jsonify({"predicted_sales": round(prediction, 2)})

@app.route("/v1/predictbatch", methods=["POST"])
def predict_batch():
    uploaded_file = request.files.get("file")
    if uploaded_file is None:
        return jsonify({"error": "Please upload a CSV file."}), 400

    batch_df = pd.read_csv(uploaded_file)
    batch_df = batch_df.copy()
    if "Product_Type_Category" not in batch_df.columns and "Product_Type" in batch_df.columns:
        batch_df["Product_Type_Category"] = batch_df["Product_Type"]

    predictions = model.predict(batch_df)
    result = {str(idx): round(float(value), 2) for idx, value in enumerate(predictions)}
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
