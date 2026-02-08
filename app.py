import streamlit as st
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Future Wealth Planner",
    page_icon="💰",
    layout="wide"
)

# --- HEADER ---
st.title("Future Wealth Planner 💰")
st.write("A simple tool to visualize your financial future.")

# --- SEPARATION LINE ---
st.markdown("---")

# --- SIDEBAR FOR INPUTS ---
with st.sidebar:
    st.header("Financial Inputs")
    
    # Example Input: User's Age
    current_age = st.number_input("Your Current Age", min_value=18, max_value=100, value=30, step=1)
    
    # Example Input: Monthly Income
    monthly_income = st.number_input("Your Monthly Net Income ($)", min_value=0, value=5000, step=100)

    st.markdown("---")
    st.write("This app is for educational purposes only.")


# --- MAIN PANEL FOR VISUALS AND REPORT ---
st.header("Your Financial Forecast")

st.write(f"You are **{current_age}** years old and your monthly income is **${monthly_income:,.2f}**.")

st.info("The visual chart and report will appear here once we build the forecasting model!")

# Placeholder for the future chart
st.subheader("Portfolio Growth Over Time")
# st.line_chart(...) will go here

# Placeholder for the future report
st.subheader("Summary Report")
# st.write(...) will go here

