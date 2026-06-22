"""
Streamlit Frontend for Digital Trust Fraud Shield
Mock digital wallet interface showing real-time fraud detection
"""

import streamlit as st
import requests
import json
from datetime import datetime, timedelta
import random
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Digital Trust Wallet",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .approve-box {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .flag-box {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .block-box {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = "http://localhost:8000"

# ==================== Helper Functions ====================

def call_fraud_api(transaction_data):
    """Call the fraud detection API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/score_transaction",
            json=transaction_data,
            timeout=5
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to Fraud Detection API. Make sure it's running on port 8000.")
        return None
    except Exception as e:
        st.error(f"Error calling API: {str(e)}")
        return None

def get_action_color(action):
    """Return color based on action"""
    if action == "APPROVE":
        return "green"
    elif action == "FLAG":
        return "orange"
    else:
        return "red"

def get_action_emoji(action):
    """Return emoji based on action"""
    if action == "APPROVE":
        return "✅"
    elif action == "FLAG":
        return "⚠️"
    else:
        return "❌"

def display_result(result):
    """Display transaction result in appropriate style"""
    action = result.get('action', 'UNKNOWN')
    risk_score = result.get('risk_score', 0)
    reason = result.get('reason', '')
    
    if action == "APPROVE":
        st.markdown(f"""
        <div class="approve-box">
            <h3>✅ Transaction Approved</h3>
            <p><strong>Risk Score:</strong> {risk_score:.2%}</p>
            <p><strong>Status:</strong> Your transaction has been processed successfully.</p>
            <p><strong>Details:</strong> {reason}</p>
        </div>
        """, unsafe_allow_html=True)
    
    elif action == "FLAG":
        st.markdown(f"""
        <div class="flag-box">
            <h3>⚠️ Additional Verification Required</h3>
            <p><strong>Risk Score:</strong> {risk_score:.2%}</p>
            <p><strong>Status:</strong> We detected some unusual activity. Please verify this transaction.</p>
            <p><strong>Details:</strong> {reason}</p>
            <p>You may be asked to enter an OTP or answer security questions.</p>
        </div>
        """, unsafe_allow_html=True)
    
    else:  # BLOCK
        st.markdown(f"""
        <div class="block-box">
            <h3>❌ Transaction Declined</h3>
            <p><strong>Risk Score:</strong> {risk_score:.2%}</p>
            <p><strong>Status:</strong> This transaction has been blocked for your security.</p>
            <p><strong>Details:</strong> {reason}</p>
            <p>Please contact customer support if you believe this is an error.</p>
        </div>
        """, unsafe_allow_html=True)

# ==================== Main App ====================

st.title("💳 Digital Trust Wallet")
st.markdown("**Real-Time Fraud Detection for ASEAN Digital Payments**")

# Sidebar navigation
page = st.sidebar.radio(
    "Navigation",
    ["Make a Payment", "Transaction History", "Analytics Dashboard", "Test Scenarios"]
)

# ==================== Page 1: Make a Payment ====================

if page == "Make a Payment":
    st.header("Process a Transaction")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Transaction Details")
        
        user_id = st.text_input(
            "User ID",
            value="user_12345",
            help="Unique identifier for the user"
        )
        
        amount = st.number_input(
            "Amount (Local Currency)",
            min_value=0.01,
            value=150.50,
            step=0.01,
            help="Transaction amount"
        )
        
        merchant = st.text_input(
            "Merchant Name",
            value="Starbucks",
            help="Name of the merchant"
        )
        
        merchant_category = st.selectbox(
            "Merchant Category",
            ["food_beverage", "retail", "transport", "entertainment", "crypto", "gambling", "wire_transfer", "utilities"],
            index=0
        )
        
        device_id = st.text_input(
            "Device ID",
            value="device_abc123",
            help="Unique device identifier"
        )
    
    with col2:
        st.subheader("Location Details")
        
        # Preset locations for ASEAN
        location_presets = {
            "Manila, Philippines": (14.5995, 120.9842),
            "Bangkok, Thailand": (13.7563, 100.5018),
            "Jakarta, Indonesia": (-6.2088, 106.8456),
            "Singapore": (1.3521, 103.8198),
            "Ho Chi Minh City, Vietnam": (10.8231, 106.6297),
            "Kuala Lumpur, Malaysia": (3.1390, 101.6869),
        }
        
        location_choice = st.selectbox(
            "Select Location",
            list(location_presets.keys()),
            index=0
        )
        
        latitude, longitude = location_presets[location_choice]
        
        st.write(f"📍 **Coordinates:** {latitude:.4f}, {longitude:.4f}")
        
        ip_address = st.text_input(
            "IP Address",
            value="192.168.1.1",
            help="IP address of the transaction"
        )
        
        card_last_4 = st.text_input(
            "Card Last 4 Digits",
            value="4242",
            max_chars=4,
            help="Last 4 digits of the card"
        )
    
    # Process button
    if st.button("🚀 Process Transaction", use_container_width=True, type="primary"):
        st.divider()
        
        # Prepare transaction data
        transaction_data = {
            "user_id": user_id,
            "amount": amount,
            "merchant": merchant,
            "merchant_category": merchant_category,
            "timestamp": datetime.now().isoformat(),
            "location": {
                "latitude": latitude,
                "longitude": longitude,
                "city": location_choice.split(",")[0],
                "country": "ASEAN"
            },
            "device_id": device_id,
            "ip_address": ip_address,
            "card_last_4": card_last_4
        }
        
        # Call API
        with st.spinner("🔍 Analyzing transaction..."):
            result = call_fraud_api(transaction_data)
        
        if result:
            # Display result
            display_result(result)
            
            # Show detailed information
            st.divider()
            st.subheader("📊 Detailed Analysis")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Risk Score", f"{result['risk_score']:.1%}")
            with col2:
                st.metric("Action", result['action'])
            with col3:
                st.metric("Transaction ID", result['transaction_id'][-8:])
            with col4:
                st.metric("Model Version", result['model_version'])
            
            # Risk score gauge
            st.subheader("Risk Assessment Gauge")
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=result['risk_score'] * 100,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Fraud Risk Score (%)"},
                delta={'reference': 50},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 40], 'color': "lightgreen"},
                        {'range': [40, 70], 'color': "lightyellow"},
                        {'range': [70, 100], 'color': "lightcoral"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 70
                    }
                }
            ))
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

# ==================== Page 2: Transaction History ====================

elif page == "Transaction History":
    st.header("Recent Transactions")
    
    # Mock transaction history
    mock_transactions = [
        {"user": "user_12345", "merchant": "Starbucks", "amount": 150.50, "status": "APPROVE", "time": datetime.now() - timedelta(hours=1)},
        {"user": "user_12345", "merchant": "Amazon", "amount": 2500.00, "status": "FLAG", "time": datetime.now() - timedelta(hours=3)},
        {"user": "user_67890", "merchant": "Grab", "amount": 45.75, "status": "APPROVE", "time": datetime.now() - timedelta(hours=5)},
        {"user": "user_11111", "merchant": "Crypto Exchange", "amount": 10000.00, "status": "BLOCK", "time": datetime.now() - timedelta(hours=8)},
        {"user": "user_22222", "merchant": "7-Eleven", "amount": 25.00, "status": "APPROVE", "time": datetime.now() - timedelta(hours=12)},
    ]
    
    df = pd.DataFrame(mock_transactions)
    df['time'] = df['time'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Color status column
    status_colors = {
        "APPROVE": "✅ APPROVE",
        "FLAG": "⚠️ FLAG",
        "BLOCK": "❌ BLOCK"
    }
    df['status'] = df['status'].map(status_colors)
    
    st.dataframe(df, use_container_width=True, hide_index=True)

# ==================== Page 3: Analytics Dashboard ====================

elif page == "Analytics Dashboard":
    st.header("Fraud Detection Analytics")
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Transactions", "1,247", "+12%")
    with col2:
        st.metric("Fraud Rate", "2.3%", "-0.5%")
    with col3:
        st.metric("False Positives", "3.1%", "-1.2%")
    with col4:
        st.metric("Avg Response Time", "45ms", "⚡")
    
    st.divider()
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Transaction Status Distribution")
        status_data = {"APPROVE": 1200, "FLAG": 35, "BLOCK": 12}
        fig = px.pie(
            values=list(status_data.values()),
            names=list(status_data.keys()),
            color_discrete_map={"APPROVE": "green", "FLAG": "orange", "BLOCK": "red"}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Risk Score Distribution")
        risk_scores = [random.uniform(0, 1) for _ in range(100)]
        fig = px.histogram(
            x=risk_scores,
            nbins=20,
            title="Distribution of Risk Scores",
            labels={"x": "Risk Score", "count": "Frequency"}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Top fraud reasons
    st.subheader("Top Fraud Detection Reasons")
    fraud_reasons = {
        "High-risk merchant category": 45,
        "Impossible geographic velocity": 28,
        "Unusual transaction time": 18,
        "Large transaction amount": 15,
        "New device": 12
    }
    
    fig = px.bar(
        x=list(fraud_reasons.values()),
        y=list(fraud_reasons.keys()),
        orientation='h',
        title="Fraud Detection Triggers",
        labels={"x": "Count", "y": "Reason"}
    )
    st.plotly_chart(fig, use_container_width=True)

# ==================== Page 4: Test Scenarios ====================

elif page == "Test Scenarios":
    st.header("Test Fraud Detection Scenarios")
    st.info("Use these pre-configured scenarios to test different fraud patterns.")
    
    scenarios = {
        "✅ Legitimate Transaction": {
            "user_id": "user_12345",
            "amount": 150.50,
            "merchant": "Starbucks",
            "merchant_category": "food_beverage",
            "location": (14.5995, 120.9842),
            "device_id": "device_abc123",
            "description": "Normal purchase at a coffee shop during business hours."
        },
        "⚠️ Large Amount": {
            "user_id": "user_12345",
            "amount": 5500.00,
            "merchant": "Electronics Store",
            "merchant_category": "retail",
            "location": (14.5995, 120.9842),
            "device_id": "device_abc123",
            "description": "Unusually large purchase that may trigger verification."
        },
        "⚠️ New Device": {
            "user_id": "user_12345",
            "amount": 200.00,
            "merchant": "Supermarket",
            "merchant_category": "retail",
            "location": (14.5995, 120.9842),
            "device_id": "device_new_xyz789",
            "description": "Transaction from a device not previously used by this user."
        },
        "❌ Impossible Velocity": {
            "user_id": "user_12345",
            "amount": 300.00,
            "merchant": "Bangkok Mall",
            "merchant_category": "retail",
            "location": (13.7563, 100.5018),  # Bangkok
            "device_id": "device_abc123",
            "description": "Transaction in Bangkok immediately after Manila transaction (impossible travel)."
        },
        "❌ High-Risk Merchant": {
            "user_id": "user_12345",
            "amount": 2000.00,
            "merchant": "Crypto Exchange",
            "merchant_category": "crypto",
            "location": (14.5995, 120.9842),
            "device_id": "device_abc123",
            "description": "Transaction at a high-risk merchant category (cryptocurrency)."
        },
        "❌ Midnight Transaction": {
            "user_id": "user_12345",
            "amount": 500.00,
            "merchant": "Wire Transfer Service",
            "merchant_category": "wire_transfer",
            "location": (14.5995, 120.9842),
            "device_id": "device_abc123",
            "description": "Suspicious wire transfer at 3:00 AM from high-risk merchant."
        }
    }
    
    selected_scenario = st.selectbox(
        "Select a Test Scenario",
        list(scenarios.keys())
    )
    
    scenario = scenarios[selected_scenario]
    st.write(f"**Description:** {scenario['description']}")
    
    if st.button("🧪 Run Test Scenario", use_container_width=True, type="primary"):
        st.divider()
        
        transaction_data = {
            "user_id": scenario["user_id"],
            "amount": scenario["amount"],
            "merchant": scenario["merchant"],
            "merchant_category": scenario["merchant_category"],
            "timestamp": datetime.now().isoformat(),
            "location": {
                "latitude": scenario["location"][0],
                "longitude": scenario["location"][1],
                "city": "Test City",
                "country": "ASEAN"
            },
            "device_id": scenario["device_id"],
            "ip_address": "192.168.1.1",
            "card_last_4": "4242"
        }
        
        with st.spinner("🔍 Analyzing transaction..."):
            result = call_fraud_api(transaction_data)
        
        if result:
            display_result(result)
            
            st.divider()
            st.subheader("📊 Detailed Analysis")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Risk Score", f"{result['risk_score']:.1%}")
            with col2:
                st.metric("Action", result['action'])
            with col3:
                st.metric("Model Version", result['model_version'])
            
            # Show raw JSON response
            with st.expander("📋 Raw API Response"):
                st.json(result)

# ==================== Footer ====================

st.divider()
st.markdown("""
---
**Digital Trust Fraud Shield** | Real-time fraud detection for ASEAN digital wallets
- 🔒 Privacy-first design
- ⚡ Sub-100ms response times
- 🌏 Optimized for ASEAN markets
""")
