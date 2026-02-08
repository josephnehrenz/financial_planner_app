import streamlit as st
import pandas as pd
import datetime

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Future Wealth Planner",
    page_icon="💰",
    layout="wide"
)

# --- HEADER ---
st.title("Future Wealth Planner 💰")
st.write("A tool to forecast your financial future based on detailed inputs.")
st.markdown("---")

# --- SIDEBAR FOR GLOBAL ASSUMPTIONS ---
with st.sidebar:
    st.header("Global Assumptions")
    
    current_age = st.number_input("Your Current Age", min_value=18, max_value=100, value=30, step=1)
    retirement_age = st.number_input("Target Retirement Age", min_value=40, max_value=100, value=65, step=1)
    # These are not used yet, but are good to have for later
    inflation_rate = st.slider("Assumed Annual Inflation Rate (%)", 0.0, 5.0, 2.5, 0.1)
    investment_return = st.slider("Assumed Annual Investment Return (%)", 0.0, 15.0, 7.0, 0.1)
    
    st.markdown("---")
    
    # Using a form helps prevent the app from re-running on every single input change
    with st.form("calculation_form"):
        submitted = st.form_submit_button("Calculate Financial Future")

# --- MAIN PANEL WITH TABS FOR INPUTS ---
tab1, tab2, tab3, tab4 = st.tabs(["💰 Income", "📈 Assets & Investments", "💸 Expenses", "🏡 Life Events"])

with tab1:
    st.header("Income Sources")
    st.write("Detail all sources of income, current and future. You can rename each source.")
    
    # --- Primary & Secondary Jobs ---
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Primary Job")
        job1_name = st.text_input("Source Name", "Primary Job - Accountant", key="job1_name")
        job1_income = st.number_input("Current Annual Salary ($)", min_value=0, value=75000, step=1000, key="job1_income")
        job1_growth = st.slider("Annual Salary Growth Rate (%)", 0.0, 10.0, 3.0, 0.1, key="job1_growth")
    
    with c2:
        st.subheader("Secondary Job")
        job2_name = st.text_input("Source Name", "Secondary Job - Consulting", key="job2_name")
        job2_income = st.number_input("Current Annual Salary ($)", min_value=0, value=15000, step=1000, key="job2_income")
        job2_growth = st.slider("Annual Salary Growth Rate (%)", 0.0, 10.0, 2.0, 0.1, key="job2_growth")

    st.markdown("---")

    # --- Expander for other income sources ---
    with st.expander("Add Future Income (Pensions, Social Security, etc.)"):
        c3, c4, c5 = st.columns(3)
        with c3:
            st.subheader("Social Security")
            ss_name = st.text_input("Source Name", "Social Security", key="ss_name", disabled=True)
            ss_start_age = st.number_input("Start Age", min_value=62, max_value=70, value=67, key="ss_start")
            ss_annual_amount = st.number_input("Estimated Annual Amount ($)", min_value=0, value=24000, step=100, key="ss_amount")

        with c4:
            st.subheader("Pension 1")
            pension1_name = st.text_input("Source Name", "Pension 1 - Military", key="pension1_name")
            pension1_start_age = st.number_input("Start Age", min_value=40, max_value=80, value=55, key="p1_start")
            pension1_annual_amount = st.number_input("Annual Amount ($)", min_value=0, value=30000, step=100, key="p1_amount")

        with c5:
            st.subheader("Pension 2")
            pension2_name = st.text_input("Source Name", "Pension 2 - Corporate", key="pension2_name")
            pension2_start_age = st.number_input("Start Age", min_value=40, max_value=80, value=65, key="p2_start")
            pension2_annual_amount = st.number_input("Annual Amount ($)", min_value=0, value=12000, step=100, key="p2_amount")

# Other tabs remain unchanged for now
with tab2:
    st.header("Assets & Investments")
    st.info("Functionality for this tab will be built next.")
with tab3:
    st.header("Expenses")
    st.info("Functionality for this tab will be built next.")
with tab4:
    st.header("Major Life Events")
    st.info("Functionality for this tab will be built next.")

# --- CALCULATION AND REPORTING ---
if submitted:
    st.markdown("---")
    st.header("Your 30-Year Income Forecast")
    
    # Set up the forecast period
    forecast_years = 30
    start_year = datetime.date.today().year
    years = list(range(start_year, start_year + forecast_years + 1))
    ages = list(range(current_age, current_age + forecast_years + 1))

    # --- Build the Income DataFrame ---
    # Create an empty DataFrame
    income_df = pd.DataFrame(index=years)
    income_df['Age'] = ages

    # 1. Job 1 Income
    current_job1_income = job1_income
    job1_incomes = []
    for age in ages:
        if age < retirement_age:
            job1_incomes.append(current_job1_income)
            current_job1_income *= (1 + job1_growth / 100)
        else:
            job1_incomes.append(0)
    income_df[job1_name] = job1_incomes
    
    # 2. Job 2 Income
    current_job2_income = job2_income
    job2_incomes = []
    for age in ages:
        if age < retirement_age:
            job2_incomes.append(current_job2_income)
            current_job2_income *= (1 + job2_growth / 100)
        else:
            job2_incomes.append(0)
    income_df[job2_name] = job2_incomes

    # 3. Social Security
    income_df[ss_name] = [ss_annual_amount if age >= ss_start_age else 0 for age in ages]

    # 4. Pension 1
    income_df[pension1_name] = [pension1_annual_amount if age >= pension1_start_age else 0 for age in ages]
    
    # 5. Pension 2
    income_df[pension2_name] = [pension2_annual_amount if age >= pension2_start_age else 0 for age in ages]

    # --- Display the Results ---
    # Create a 'Total Income' column
    income_columns = [job1_name, job2_name, ss_name, pension1_name, pension2_name]
    income_df['Total Income'] = income_df[income_columns].sum(axis=1)

    # Set the index to 'Age' for better charting
    chart_df = income_df.set_index('Age')

    st.subheader("Income Streams Over Time")
    st.line_chart(chart_df[income_columns + ['Total Income']])
    
    st.subheader("Income Data Table")
    # Format the dataframe for better display
    display_df = chart_df.copy()
    for col in display_df.columns:
        display_df[col] = display_df[col].apply(lambda x: f"${x:,.0f}")
    st.dataframe(display_df)
