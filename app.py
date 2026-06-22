import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/risk-score"

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Smart Wallet Guardian", layout="wide")

# ------------------ CUSTOM UI ------------------
st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
    }
    .block-container {
        padding-top: 2rem;
    }
    .stButton>button {
        border-radius: 10px;
        height: 3em;
        width: 100%;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------
st.markdown("## 💳 Smart Wallet Guardian")
st.markdown("### 🔍 AI Fraud Detection Dashboard")
st.markdown("---")

st.info("💡 This system analyzes transactions in real time and flags suspicious activity using risk scoring.")

# ------------------ DEFAULT VALUES ------------------
if "amount" not in st.session_state:
    st.session_state.amount = 120.0
    st.session_state.time_value = 12000.0
    st.session_state.frequency = 1
    st.session_state.new_device = "No"
    st.session_state.location_risk = "Low"
    st.session_state.odd_hour = "No"

# ------------------ SAMPLE BUTTONS ------------------
def load_safe():
    st.session_state.amount = 80.0
    st.session_state.time_value = 14000.0
    st.session_state.frequency = 1
    st.session_state.new_device = "No"
    st.session_state.location_risk = "Low"
    st.session_state.odd_hour = "No"

def load_fraud():
    st.session_state.amount = 3500.0
    st.session_state.time_value = 150.0
    st.session_state.frequency = 12
    st.session_state.new_device = "Yes"
    st.session_state.location_risk = "High"
    st.session_state.odd_hour = "Yes"

# ------------------ LAYOUT ------------------
left, right = st.columns([1, 1])

# ------------------ INPUT PANEL ------------------
with left:
    st.subheader("🧾 Transaction Details")

    c1, c2 = st.columns(2)
    c1.button("✅ Safe Example", on_click=load_safe)
    c2.button("🚨 Fraud Example", on_click=load_fraud)

    st.markdown("---")

    amount = st.number_input("Transaction Amount (RM)", min_value=0.0, step=10.0, key="amount")
    time_value = st.number_input("Transaction Time", min_value=0.0, step=100.0, key="time_value")

    frequency = st.slider("Transactions in Last 24 Hours", 0, 20, key="frequency")

    new_device = st.selectbox("New Device?", ["No", "Yes"], key="new_device")
    location_risk = st.selectbox("Location Risk", ["Low", "Medium", "High"], key="location_risk")
    odd_hour = st.selectbox("Unusual Hour?", ["No", "Yes"], key="odd_hour")

# ------------------ RESULT PANEL ------------------
with right:
    st.subheader("📊 Analysis Result")

    if st.button("🚀 Analyze Transaction", use_container_width=True):

        payload = {
            "amount": float(amount),
            "time_value": float(time_value),
            "frequency": int(frequency),
            "new_device": True if new_device == "Yes" else False,
            "location_risk": location_risk,
            "odd_hour": True if odd_hour == "Yes" else False
        }

        try:
            response = requests.post(API_URL, json=payload, timeout=10)

            if response.status_code == 200:
                result = response.json()

                decision = result["decision"]
                score = result["risk_score"]
                level = result["risk_level"]
                reasons = result["reasons"]

                # -------- COLOR LOGIC --------
                if level == "Low":
                    color = "green"
                elif level == "Medium":
                    color = "orange"
                else:
                    color = "red"

                # -------- DECISION DISPLAY --------
                st.markdown(f"""
                ### 🧾 Decision: <span style='color:{color}'>{decision}</span>
                """, unsafe_allow_html=True)

                if decision == "APPROVE":
                    st.toast("✅ Transaction Approved")
                elif decision == "FLAG":
                    st.toast("⚠️ Transaction Flagged")
                else:
                    st.toast("🚫 Transaction Blocked")

                # -------- METRICS --------
                c1, c2 = st.columns(2)
                c1.metric("Risk Score", f"{score}%")
                c2.metric("Risk Level", level)

                # -------- PROGRESS BAR --------
                st.progress(score / 100)

                st.markdown("---")

                # -------- REASONS --------
                st.markdown("### 🔎 Why was this flagged?")
                for reason in reasons:
                    st.markdown(f"✔️ {reason}")

                st.markdown("---")

                # -------- VALUE SECTION --------
                st.markdown("### 💼 Product Value")
                st.markdown("✔️ Reduces fraud losses")
                st.markdown("✔️ Real-time decision support")
                st.markdown("✔️ Explainable AI output")

            else:
                st.error(f"API error: {response.status_code}")

        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to backend. Run: python -m uvicorn fraud_api:app --reload")

        except Exception as e:
            st.error(f"Unexpected error: {e}")
