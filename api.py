import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

MODEL_PATH = "models/fraud_detection_model.pkl"
FEATURE_PATH = "models/model_features.pkl"

# Load trained model artifacts
model = joblib.load(MODEL_PATH)
feature_columns = joblib.load(FEATURE_PATH)

app = FastAPI(title="Smart Wallet Guardian API")


class TransactionRequest(BaseModel):
    amount: float
    time_value: float
    frequency: int
    new_device: bool
    location_risk: str
    odd_hour: bool


def build_feature_row(payload: TransactionRequest) -> pd.DataFrame:
    """
    Build a single-row dataframe matching the exact feature columns
    expected by the trained model.
    """
    row = {col: 0.0 for col in feature_columns}

    # Real dataset columns
    if "Time" in row:
        row["Time"] = float(payload.time_value)

    if "Amount" in row:
        row["Amount"] = float(payload.amount)

    # Demo-friendly mapping into anonymized features
    # These are proxy mappings so the live demo can work with user-friendly inputs.
    if "V1" in row:
        row["V1"] = -1.2 if payload.new_device else 0.2

    if "V2" in row:
        row["V2"] = 1.0 if payload.odd_hour else -0.1

    if "V3" in row:
        row["V3"] = -1.0 if payload.frequency >= 8 else 0.1

    if "V4" in row:
        row["V4"] = 1.2 if payload.location_risk == "High" else (0.5 if payload.location_risk == "Medium" else 0.0)

    if "V5" in row:
        row["V5"] = 1.1 if payload.amount > 2000 else (0.4 if payload.amount > 1000 else 0.0)

    if "V6" in row:
        row["V6"] = -0.6 if payload.new_device and payload.odd_hour else 0.0

    if "V7" in row:
        row["V7"] = 1.0 if payload.frequency >= 12 else 0.0

    if "V8" in row:
        row["V8"] = 0.8 if payload.location_risk == "High" and payload.odd_hour else 0.0

    return pd.DataFrame([row])[feature_columns]


def calculate_logic_score(payload: TransactionRequest) -> int:
    """
    Business-rule layer used together with ML probability
    to make the demo more interpretable.
    """
    score = 0

    if payload.amount > 3000:
        score += 35
    elif payload.amount > 1500:
        score += 20
    elif payload.amount > 800:
        score += 10

    if payload.frequency >= 12:
        score += 20
    elif payload.frequency >= 8:
        score += 10

    if payload.new_device:
        score += 15

    if payload.location_risk == "Medium":
        score += 10
    elif payload.location_risk == "High":
        score += 20

    if payload.odd_hour:
        score += 15

    return min(score, 100)


def get_risk_level_and_decision(score: int):
    if score < 30:
        return "LOW", "APPROVE"
    if score < 65:
        return "MEDIUM", "FLAG"
    return "HIGH", "BLOCK"


def generate_reasons(payload: TransactionRequest, final_score: int):
    reasons = []

    if payload.amount > 1500:
        reasons.append("High transaction amount")

    if payload.frequency >= 8:
        reasons.append("Unusual transaction frequency")

    if payload.new_device:
        reasons.append("New device detected")

    if payload.location_risk == "Medium":
        reasons.append("Medium-risk location pattern")
    elif payload.location_risk == "High":
        reasons.append("High-risk location pattern")

    if payload.odd_hour:
        reasons.append("Transaction at unusual hour")

    if final_score >= 65:
        reasons.append("Combined risk pattern is strongly suspicious")

    if not reasons:
        reasons.append("No strong suspicious indicators")

    return reasons


@app.get("/")
def root():
    return {"message": "Smart Wallet Guardian API is running with ML model"}


@app.post("/risk-score")
def risk_score(payload: TransactionRequest):
    input_df = build_feature_row(payload)

    # ML prediction
    model_prob = float(model.predict_proba(input_df)[0][1])

    # Business logic score
    logic_score = calculate_logic_score(payload)

    # Blend both for a more stable demo
    final_score = int((model_prob * 100 * 0.5) + (logic_score * 0.5))

    risk_level, decision = get_risk_level_and_decision(final_score)

    return {
        "risk_score": final_score,
        "risk_level": risk_level,
        "decision": decision,
        "model_probability": round(model_prob, 4),
        "reasons": generate_reasons(payload, final_score)
    }
