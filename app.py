import streamlit as st
import pandas as pd
import datetime
import altair as alt

# --- PAGE CONFIG ---
st.set_page_config(page_title="Future Wealth Planner", page_icon="💰", layout="wide")

# --- INITIALIZE SESSION STATE ---
# We still need session state to know *when* to draw the report, but not to create the tab
if 'report_ready' not in st.session_state:
    st.session_state.report_ready = False

def run_calculation():
    """Sets the flag to show the report content."""
    st.session_state.report_ready = True

# --- HEADER ---
st.title("Future Wealth Planner 💰")
st.write("A tool to forecast your financial future based on detailed inputs.")
st.markdown("---")

# --- SIDEBAR FOR GLOBAL ASSUMPTIONS ---
with st.sidebar:
    st.header("Global Assumptions")
    current_age = st.number_input("Your Current Age", 18, 100, 30, 1)
    retirement_age = st.number_input("Target Retirement Age", 40, 100, 65, 1)
    forecast_length = st.number_input("Forecast Length (Years)", 5, 60, 30, 1)
    inflation_rate = st.slider("Assumed Annual Inflation Rate (%)", 0.0, 5.0, 2.5, 0.1)
    investment_return = st.slider("Assumed Annual Investment Return (%)", 0.0, 15.0, 7.0, 0.1)
    st.markdown("---")
    st.button("Calculate Financial Future", on_click=run_calculation, use_container_width=True, type="primary")

# --- DEFINE TABS (Now static, as per your suggestion) ---
tab_income, tab_assets, tab_expenses, tab_events, tab_report = st.tabs([
    "💰 Income", "📈 Assets & Investments", "💸 Expenses", "🏡 Life Events", "📊 Forecast & Report"
])

# --- INPUT TABS ---
with tab_income:
    st.header("Income Sources"); st.write("Detail all sources of income. Uncheck any source to exclude it from the forecast.")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Primary Job"); inc_job1 = st.checkbox("Include in Forecast", True, key="inc_job1")
        job1_name = st.text_input("Source Name", "Primary Job", key="job1_name")
        job1_income = st.number_input("Current Annual Salary ($)", 0, None, 75000, 1000, key="job1_income")
        job1_growth = st.slider("Annual Salary Growth Rate (%)", 0.0, 10.0, 3.0, 0.1, key="job1_growth")
    with c2:
        st.subheader("Secondary Job"); inc_job2 = st.checkbox("Include in Forecast", True, key="inc_job2")
        job2_name = st.text_input("Source Name", "Side Hustle", key="job2_name")
        job2_income = st.number_input("Current Annual Salary ($)", 0, None, 15000, 1000, key="job2_income")
        job2_growth = st.slider("Annual Salary Growth Rate (%)", 0.0, 10.0, 2.0, 0.1, key="job2_growth")
    st.markdown("---")
    with st.expander("Add Future Income (Pensions, Social Security, etc.)"):
        c3, c4, c5 = st.columns(3)
        with c3:
            st.subheader("Social Security"); inc_ss = st.checkbox("Include in Forecast", True, key="inc_ss")
            ss_name = st.text_input("Source Name", "Social Security", key="ss_name", disabled=True)
            ss_start_age = st.number_input("Start Age", 62, 70, 67, key="ss_start")
            ss_annual_amount = st.number_input("Estimated Annual Amount ($)", 0, None, 24000, 100, key="ss_amount")
        with c4:
            st.subheader("Pension 1"); inc_pension1 = st.checkbox("Include in Forecast", True, key="inc_p1")
            pension1_name = st.text_input("Source Name", "Military Pension", key="pension1_name")
            pension1_start_age = st.number_input("Start Age", 40, 80, 55, key="p1_start")
            pension1_annual_amount = st.number_input("Annual Amount ($)", 0, None, 30000, 100, key="p1_amount")
        with c5:
            st.subheader("Pension 2"); inc_pension2 = st.checkbox("Include in Forecast", False, key="inc_p2")
            pension2_name = st.text_input("Source Name", "Corporate Pension", key="pension2_name")
            pension2_start_age = st.number_input("Start Age", 40, 80, 65, key="p2_start")
            pension2_annual_amount = st.number_input("Annual Amount ($)", 0, None, 12000, 100, key="p2_amount")

with tab_assets: st.header("Assets & Investments"); st.info("Functionality for this tab will be built next.")
with tab_expenses: st.header("Expenses"); st.info("Functionality for this tab will be built next.")
with tab_events: st.header("Major Life Events"); st.info("Functionality for this tab will be built next.")

# --- REPORTING TAB ---
with tab_report:
    st.header("Your Financial Forecast")
    if not st.session_state.report_ready:
        st.info("Click the 'Calculate Financial Future' button in the sidebar to generate your forecast.")
    else:
        # --- Data Preparation ---
        start_year = datetime.date.today().year; years = list(range(start_year, start_year + forecast_length + 1)); ages = list(range(current_age, current_age + forecast_length + 1))
        income_df = pd.DataFrame(index=years, data={'Age': ages}); event_list = []
        if inc_job1:
            job1_incomes = [(job1_income * (1 + job1_growth / 100)**i) if age < retirement_age else 0 for i, age in enumerate(ages)]; income_df[job1_name] = job1_incomes
            if retirement_age in ages and any(v > 0 for v in job1_incomes):
                retirement_index = ages.index(retirement_age);
                if retirement_index > 0: event_list.append({'Age': retirement_age, 'Value': job1_incomes[retirement_index - 1], 'Event': f'{job1_name} Ends', 'Color': '#d62728'})
        if inc_job2:
            job2_incomes = [(job2_income * (1 + job2_growth / 100)**i) if age < retirement_age else 0 for i, age in enumerate(ages)]; income_df[job2_name] = job2_incomes
            if retirement_age in ages and any(v > 0 for v in job2_incomes):
                retirement_index = ages.index(retirement_age)
                if retirement_index > 0: event_list.append({'Age': retirement_age, 'Value': job2_incomes[retirement_index - 1], 'Event': f'{job2_name} Ends', 'Color': '#d62728'})
        if inc_ss:
            income_df[ss_name] = [ss_annual_amount if age >= ss_start_age else 0 for age in ages]
            if ss_annual_amount > 0 and ss_start_age in ages: event_list.append({'Age': ss_start_age, 'Value': 0, 'Event': f'{ss_name} Begins', 'Color': '#2ca02c'})
        if inc_pension1:
            income_df[pension1_name] = [pension1_annual_amount if age >= pension1_start_age else 0 for age in ages]
            if pension1_annual_amount > 0 and pension1_start_age in ages: event_list.append({'Age': pension1_start_age, 'Value': 0, 'Event': f'{pension1_name} Begins', 'Color': '#2ca02c'})
        if inc_pension2:
            income_df[pension2_name] = [pension2_annual_amount if age >= pension2_start_age else 0 for age in ages]
            if pension2_annual_amount > 0 and pension2_start_age in ages: event_list.append({'Age': pension2_start_age, 'Value': 0, 'Event': f'{pension2_name} Begins', 'Color': '#2ca02c'})
        
        income_columns = [c for c in [job1_name, job2_name, ss_name, pension1_name, pension2_name] if c in income_df.columns and not income_df[c].empty]
        if income_columns: income_df['Total Income'] = income_df[income_columns].sum(axis=1)
        else: income_df['Total Income'] = 0
        df_melted = income_df.reset_index().melt(id_vars=['index', 'Age'], value_vars=income_columns + ['Total Income'], var_name='Source', value_name='Value'); df_melted.rename(columns={'index':'Year'}, inplace=True)
        
        # --- Charting ---
        line_chart = alt.Chart(df_melted).mark_line(size=3).encode(
            x=alt.X('Age:O', title='Your Age'), y=alt.Y('Value:Q', title='Annual Income', axis=alt.Axis(format='$,.0f')), color='Source:N', tooltip=['Year', 'Age', 'Source', alt.Tooltip('Value:Q', format='$,.0f')]
        ).properties(title='Income Streams and Life Events Over Time')
        
        # *** FINAL FIX: Layering logic is now robust ***
        if event_list:
            events_df = pd.DataFrame(event_list)
            event_markers = alt.Chart(events_df).mark_circle(size=150, stroke='white', strokeWidth=2).encode(
                x=alt.X('Age:O'), y=alt.Y('Value:Q'), color=alt.Color('Color:N', scale=None), tooltip=['Age', 'Event']
            )
            final_chart = alt.layer(line_chart, event_markers) # The problematic .resolve_scale() is removed
        else:
            final_chart = line_chart # If no events, the chart is just the lines

        st.altair_chart(final_chart.interactive(), use_container_width=True)

        # --- Summary Report ---
        st.subheader("Narrative Summary")
        if not income_df.empty and 'Total Income' in income_df.columns and not income_df['Total Income'].empty:
            peak_income_year = income_df['Total Income'].idxmax(); peak_income_value = income_df['Total Income'].max(); total_lifetime_income = income_df['Total Income'].sum()
            st.write(f"- Your forecast runs for **{forecast_length}** years, from age **{current_age}** to **{ages[-1]}**.")
            if peak_income_value > 0: st.write(f"- Your income is projected to peak in **{peak_income_year}** at age **{income_df.loc[peak_income_year, 'Age']}**, reaching **${peak_income_value:,.0f}**.")
            st.write(f"- Over this period, your total estimated income is **${total_lifetime_income:,.0f}**.")
        else: st.warning("No income sources were included in the forecast.")

        # --- Data Table ---
        with st.expander("View Detailed Income Data Table"):
            display_df = income_df.set_index('Age').copy();
            for col in display_df.columns: display_df[col] = display_df[col].apply(lambda x: f"${x:,.0f}")
            st.dataframe(display_df, use_container_width=True)
