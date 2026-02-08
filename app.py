import streamlit as st
import pandas as pd
import datetime
import altair as alt

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
    forecast_length = st.number_input("Forecast Length (Years)", min_value=5, max_value=60, value=30, step=1)
    
    # These are not used yet, but are good to have for later
    inflation_rate = st.slider("Assumed Annual Inflation Rate (%)", 0.0, 5.0, 2.5, 0.1)
    investment_return = st.slider("Assumed Annual Investment Return (%)", 0.0, 15.0, 7.0, 0.1)
    
    st.markdown("---")
    
    with st.form("calculation_form"):
        submitted = st.form_submit_button("Calculate Financial Future")

# --- MAIN PANEL WITH TABS FOR INPUTS ---
st.write("## Step 1: Enter Your Financial Details")
tab1, tab2, tab3, tab4 = st.tabs(["💰 Income", "📈 Assets & Investments", "💸 Expenses", "🏡 Life Events"])

with tab1:
    st.header("Income Sources")
    st.write("Detail all sources of income. Uncheck any source to exclude it from the forecast.")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Primary Job")
        inc_job1 = st.checkbox("Include in Forecast", value=True, key="inc_job1")
        job1_name = st.text_input("Source Name", "Primary Job", key="job1_name")
        job1_income = st.number_input("Current Annual Salary ($)", min_value=0, value=75000, step=1000, key="job1_income")
        job1_growth = st.slider("Annual Salary Growth Rate (%)", 0.0, 10.0, 3.0, 0.1, key="job1_growth")
    
    with c2:
        st.subheader("Secondary Job")
        inc_job2 = st.checkbox("Include in Forecast", value=True, key="inc_job2")
        job2_name = st.text_input("Source Name", "Side Hustle", key="job2_name")
        job2_income = st.number_input("Current Annual Salary ($)", min_value=0, value=15000, step=1000, key="job2_income")
        job2_growth = st.slider("Annual Salary Growth Rate (%)", 0.0, 10.0, 2.0, 0.1, key="job2_growth")

    st.markdown("---")

    with st.expander("Add Future Income (Pensions, Social Security, etc.)"):
        c3, c4, c5 = st.columns(3)
        with c3:
            st.subheader("Social Security")
            inc_ss = st.checkbox("Include in Forecast", value=True, key="inc_ss")
            ss_name = st.text_input("Source Name", "Social Security", key="ss_name", disabled=True)
            ss_start_age = st.number_input("Start Age", min_value=62, max_value=70, value=67, key="ss_start")
            ss_annual_amount = st.number_input("Estimated Annual Amount ($)", min_value=0, value=24000, step=100, key="ss_amount")

        with c4:
            st.subheader("Pension 1")
            inc_pension1 = st.checkbox("Include in Forecast", value=True, key="inc_p1")
            pension1_name = st.text_input("Source Name", "Military Pension", key="pension1_name")
            pension1_start_age = st.number_input("Start Age", min_value=40, max_value=80, value=55, key="p1_start")
            pension1_annual_amount = st.number_input("Annual Amount ($)", min_value=0, value=30000, step=100, key="p1_amount")

        with c5:
            st.subheader("Pension 2")
            inc_pension2 = st.checkbox("Include in Forecast", value=False, key="inc_p2")
            pension2_name = st.text_input("Source Name", "Corporate Pension", key="pension2_name")
            pension2_start_age = st.number_input("Start Age", min_value=40, max_value=80, value=65, key="p2_start")
            pension2_annual_amount = st.number_input("Annual Amount ($)", min_value=0, value=12000, step=100, key="p2_amount")

with tab2:
    st.header("Assets & Investments"); st.info("Functionality for this tab will be built next.")
with tab3:
    st.header("Expenses"); st.info("Functionality for this tab will be built next.")
with tab4:
    st.header("Major Life Events"); st.info("Functionality for this tab will be built next.")

# --- CALCULATION & REPORTING LOGIC (runs only when button is clicked) ---
if submitted:
    # --- Data Preparation ---
    start_year = datetime.date.today().year
    years = list(range(start_year, start_year + forecast_length + 1))
    ages = list(range(current_age, current_age + forecast_length + 1))
    
    income_df = pd.DataFrame(index=years)
    income_df['Age'] = ages
    
    event_list = []

    # --- Income Calculations ---
    # Job 1
    if inc_job1:
        job1_incomes = [(job1_income * (1 + job1_growth / 100)**i) if age < retirement_age else 0 for i, age in enumerate(ages)]
        income_df[job1_name] = job1_incomes
        if any(v > 0 for v in job1_incomes): event_list.append({'Age': retirement_age, 'Event': f'{job1_name} Ends', 'Color': 'red'})
    else: income_df[job1_name] = 0
    # Job 2
    if inc_job2:
        job2_incomes = [(job2_income * (1 + job2_growth / 100)**i) if age < retirement_age else 0 for i, age in enumerate(ages)]
        income_df[job2_name] = job2_incomes
        if any(v > 0 for v in job2_incomes): event_list.append({'Age': retirement_age, 'Event': f'{job2_name} Ends', 'Color': 'red'})
    else: income_df[job2_name] = 0
    # Social Security
    if inc_ss:
        income_df[ss_name] = [ss_annual_amount if age >= ss_start_age else 0 for age in ages]
        if ss_annual_amount > 0: event_list.append({'Age': ss_start_age, 'Event': f'{ss_name} Begins', 'Color': 'green'})
    else: income_df[ss_name] = 0
    # Pension 1
    if inc_pension1:
        income_df[pension1_name] = [pension1_annual_amount if age >= pension1_start_age else 0 for age in ages]
        if pension1_annual_amount > 0: event_list.append({'Age': pension1_start_age, 'Event': f'{pension1_name} Begins', 'Color': 'green'})
    else: income_df[pension1_name] = 0
    # Pension 2
    if inc_pension2:
        income_df[pension2_name] = [pension2_annual_amount if age >= pension2_start_age else 0 for age in ages]
        if pension2_annual_amount > 0: event_list.append({'Age': pension2_start_age, 'Event': f'{pension2_name} Begins', 'Color': 'green'})
    else: income_df[pension2_name] = 0
    
    income_columns = [c for c in [job1_name, job2_name, ss_name, pension1_name, pension2_name] if c in income_df.columns]
    income_df['Total Income'] = income_df[income_columns].sum(axis=1)

    # --- Melt DataFrame for Altair ---
    df_melted = income_df.reset_index().melt(id_vars=['index', 'Age'], value_vars=income_columns + ['Total Income'], var_name='Source', value_name='Value')
    df_melted.rename(columns={'index':'Year'}, inplace=True)

    # --- Charting ---
    st.markdown("---")
    st.write("## 📊 Your Financial Forecast")

    # Base chart
    base = alt.Chart(df_melted).encode(x=alt.X('Age:O', title='Your Age'))

    # Line chart for income streams
    line_chart = base.mark_line().encode(
        y=alt.Y('Value:Q', title='Annual Income', axis=alt.Axis(format='$,.0f')),
        color='Source:N',
        tooltip=['Year', 'Age', 'Source', alt.Tooltip('Value:Q', format='$,.0f')]
    ).interactive()

    # Event markers
    events_df = pd.DataFrame(event_list)
    event_markers = alt.Chart(events_df).mark_circle(
        size=100,
        stroke='black',
        strokeWidth=1
    ).encode(
        x=alt.X('Age:O'),
        color=alt.Color('Color:N', scale=None), # Use the color directly from the dataframe
        tooltip=['Age', 'Event']
    ).properties(
        title='Income Streams and Life Events Over Time'
    )

    # Combine chart and markers
    final_chart = (line_chart + event_markers).resolve_scale(y='shared')
    st.altair_chart(final_chart, use_container_width=True)

    # --- Summary Report ---
    st.subheader("Narrative Summary")
    peak_income_year = income_df['Total Income'].idxmax()
    peak_income_value = income_df['Total Income'].max()
    total_lifetime_income = income_df['Total Income'].sum()

    st.write(f"""
    - Your forecast runs for **{forecast_length}** years, from age **{current_age}** to **{ages[-1]}**.
    - Your income is projected to peak in the year **{peak_income_year}** at age **{income_df.loc[peak_income_year, 'Age']}**, reaching **${peak_income_value:,.0f}**.
    - Over this period, your total estimated income from all included sources is **${total_lifetime_income:,.0f}**.
    """)

    # --- Data Table ---
    with st.expander("View Detailed Income Data Table"):
        display_df = income_df.set_index('Age')
        for col in display_df.columns: display_df[col] = display_df[col].apply(lambda x: f"${x:,.0f}")
        st.dataframe(display_df)
