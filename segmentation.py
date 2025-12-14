# import streamlit as st
# import pandas as pd
# import numpy as np
# import joblib
#
# kmeans = joblib.load("models/kmeans_model.pkl")
# scaler = joblib.load("scalers/scaler.pkl")
#
# st.title("Customer Segmentation App")
# st.write("Enter customer details to predict the segment.")
#
# age = st.number_input("Age", min_value=18, max_value=100, value=35)
# income = st.number_input("Income", min_value=0, max_value=200000, value=50000)
# total_spending = st.number_input("Total Spending (sum of purchases)", min_value=0, max_value=10000, value=1000)
# num_web_purchases = st.number_input("Number of Web Purchases", min_value=0, max_value=100, value=10)
# num_store_purchases = st.number_input("Number of Store Purchases", min_value=0, max_value=100, value=10)
# num_web_visits = st.number_input("Number of Web Visits (per Month)", min_value=0, max_value=100, value=5)
# recency = st.number_input("Recency (days since last purchase)", min_value=0, max_value=365, value=30)
#
# input_data = pd.DataFrame({
#     "Age": [age],
#     "Income": [income],
#     "Total_Spending": [total_spending],
#     "NumWebPurchases": [num_web_purchases],
#     "NumStorePurchases": [num_store_purchases],
#     "NumWebVisitsMonth": [num_web_visits],
#     "Recency": [recency],
# })
#
# input_scaled = scaler.transform(input_data)
#
# if st.button("Predict Segment"):
#     cluster = kmeans.predict(input_scaled)[0]
#
#     st.success(f"Predicted segment: Cluster {cluster}")

import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load models and data
kmeans = joblib.load("models/kmeans_model.pkl")
scaler = joblib.load("scalers/scaler.pkl")
cluster_summary = pd.read_csv("data/cluster_summary.csv")

# Segment descriptions and strategies (manual configuration)
SEGMENT_DESCRIPTIONS = {
    0: {
        "name": "Casual Shoppers",
        "description": "Younger customers with low income and minimal spending",
        "strategy": "Strategy: Promotional offers, discount codes, free shipping",
        "color": "#FF6B6B"
    },
    1: {
        "name": "VIP Customers",
        "description": "Most valuable segment with highest spending",
        "strategy": "Strategy: Premium loyalty programs, exclusive offers, early access",
        "color": "#FFD700"
    },
    2: {
        "name": "Browsers Without Conversion",
        "description": "Interested but not purchasing",
        "strategy": "Strategy: Urgent reactivation campaign, personalized offers, win-back emails",
        "color": "#FFA07A"
    },
    3: {
        "name": "Digital Enthusiasts",
        "description": "Active customers with high online purchases",
        "strategy": "Strategy: Optimize online UX, product recommendations, cross-selling",
        "color": "#4ECDC4"
    }
}

# User interface
st.title("Customer Segmentation App")
st.write("Enter customer details to predict the segment and receive marketing recommendations.")

st.divider()

# Form in two columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("Demographic Data")
    age = st.number_input("Age", min_value=18, max_value=100, value=35)
    income = st.number_input("Income", min_value=0, max_value=200000, value=50000)
    total_spending = st.number_input("Total Spending", min_value=0, max_value=10000, value=1000)

with col2:
    st.subheader("Purchase Behavior")
    num_web_purchases = st.number_input("Number of Web Purchases", min_value=0, max_value=100, value=10)
    num_store_purchases = st.number_input("Number of Store Purchases", min_value=0, max_value=100, value=10)
    num_web_visits = st.number_input("Web Visits per Month", min_value=0, max_value=100, value=5)
    recency = st.number_input("Days Since Last Purchase", min_value=0, max_value=365, value=30)

# Prepare input data
input_data = pd.DataFrame({
    "Age": [age],
    "Income": [income],
    "Total_Spending": [total_spending],
    "NumWebPurchases": [num_web_purchases],
    "NumStorePurchases": [num_store_purchases],
    "NumWebVisitsMonth": [num_web_visits],
    "Recency": [recency],
})

input_scaled = scaler.transform(input_data)

st.divider()

# Prediction button
if st.button("Predict Segment", type="primary", use_container_width=True):
    cluster = kmeans.predict(input_scaled)[0]
    profile = SEGMENT_DESCRIPTIONS[cluster]

    # Get segment statistics from cluster_summary
    segment_stats = cluster_summary[cluster_summary['Cluster'] == cluster].iloc[0]

    # Display result with colored background
    st.markdown(f"""
        <div style='padding: 20px; border-radius: 10px; background-color: {profile['color']}20; border-left: 5px solid {profile['color']}'>
            <h2 style='color: {profile['color']}; margin: 0;'>{profile['name']}</h2>
        </div>
    """, unsafe_allow_html=True)

    st.write("")

    # Segment description
    st.markdown(f"**{profile['description']}**")

    st.write("")

    # Characteristics in two columns
    col_char, col_strat = st.columns(2)

    with col_char:
        st.markdown("**Average Segment Characteristics:**")
        st.write(f"• Age: {segment_stats['Age']:.0f} years")
        st.write(f"• Income: ~{segment_stats['Income']:,.0f}")
        st.write(f"• Spending: ~{segment_stats['Total_Spending']:.0f}")
        st.write(f"• Web purchases: {segment_stats['NumWebPurchases']:.1f}")
        st.write(f"• Store purchases: {segment_stats['NumStorePurchases']:.1f}")
        st.write(f"• Web visits: {segment_stats['NumWebVisitsMonth']:.1f}/month")
        st.write(f"• Days since last purchase: {segment_stats['Recency']:.0f}")

    with col_strat:
        st.info(profile['strategy'])

    st.divider()

    # Additional information
    with st.expander("More Information About Segments"):
        st.write("**Comparison with Other Segments (Average Values):**")

        # Comparison table from cluster_summary
        display_summary = cluster_summary.copy()
        display_summary['Income'] = display_summary['Income'].apply(lambda x: f"{x:,.0f}")
        display_summary['Total_Spending'] = display_summary['Total_Spending'].apply(lambda x: f"{x:.0f}")
        display_summary['Age'] = display_summary['Age'].apply(lambda x: f"{x:.0f}")

        st.dataframe(display_summary, hide_index=True, use_container_width=True)

        st.write(f"**Your customer belongs to segment: {cluster}**")

# Sidebar with legend
with st.sidebar:
    st.header("Segment Legend")

    for cluster_id, profile in SEGMENT_DESCRIPTIONS.items():
        with st.expander(f"Segment {cluster_id}: {profile['name']}"):
            st.write(profile['description'])
            st.caption(profile['strategy'])