import streamlit as st
import pandas as pd
import datetime
import altair as alt

# --- PAGE CONFIG ---
st.set_page_config(page_title="Future Wealth Planner", page_icon="💰", layout="wide")

# --- INITIALIZE SESSION STATE ---
if 'report_ready' not in st.session_state:
    st.session_state.report_ready = False

def run_calculation():
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
    forecast_length = st.number_input("Forecast Length (Years)", 5, 60, 40, 1) # Extended default for long-term view
    investment_return = st.slider("Assumed Annual Investment Return (%)", 0.0, 15.0, 7.0, 0.1)
    inflation_rate = st.slider("Assumed Annual Inflation Rate (%)", 0.0, 5.0, 2.5, 0.1) # Not used yet
    st.markdown("---")
    st.button("Calculate Financial Future", on_click=run_calculation, use_container_width=True, type="primary")

# --- DEFINE TABS ---
tab_income, tab_assets, tab_expenses, tab_events, tab_report = st.tabs([
    "💰 Income", "📈 Assets & Investments", "💸 Expenses", "🏡 Life Events", "📊 Forecast & Report"
])

# --- INPUT TABS ---
with tab_income:
    # ... (Income tab code remains unchanged) ...
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

with tab_assets:
    st.header("Assets & Investments")
    st.write("Detail your financial accounts that grow over time and can be drawn upon in retirement.")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("Pre-Tax Retirement")
        inc_pretax = st.checkbox("Include in Forecast", True, key="inc_pretax")
        pretax_name = st.text_input("Account Name", "401(k)/Traditional IRA", key="pretax_name")
        pretax_balance = st.number_input("Current Balance ($)", 0, None, 50000, 1000, key="pretax_bal")
        pretax_contrib = st.number_input("Monthly Contribution ($)", 0, None, 500, 100, key="pretax_con")
        pretax_wd_rate = st.slider("Retirement Drawdown (%/yr)", 0.0, 10.0, 4.0, 0.1, key="pretax_wd")
    with c2:
        st.subheader("Roth Retirement")
        inc_roth = st.checkbox("Include in Forecast", True, key="inc_roth")
        roth_name = st.text_input("Account Name", "Roth IRA/401(k)", key="roth_name")
        roth_balance = st.number_input("Current Balance ($)", 0, None, 25000, 1000, key="roth_bal")
        roth_contrib = st.number_input("Monthly Contribution ($)", 0, None, 300, 100, key="roth_con")
        roth_wd_rate = st.slider("Retirement Drawdown (%/yr)", 0.0, 10.0, 4.0, 0.1, key="roth_wd")
    with c3:
        st.subheader("Taxable Brokerage")
        inc_brokerage = st.checkbox("Include in Forecast", True, key="inc_brokerage")
        brokerage_name = st.text_input("Account Name", "Taxable Brokerage", key="brokerage_name")
        brokerage_balance = st.number_input("Current Balance ($)", 0, None, 10000, 1000, key="brokerage_bal")
        brokerage_contrib = st.number_input("Monthly Contribution ($)", 0, None, 200, 100, key="brokerage_con")
        brokerage_wd_rate = st.slider("Retirement Drawdown (%/yr)", 0.0, 10.0, 2.0, 0.1, key="brokerage_wd")

    with st.expander("Future Feature: Required Minimum Distributions (RMDs)"):
        st.info("RMDs are complex and based on IRS tables. A future version will calculate this automatically. For now, you can approximate it using the drawdown sliders.")
        rmd_start_age = st.number_input("RMD Start Age", 70, 80, 73)
    
    with st.expander("Add Physical & Other Assets"):
        st.caption("Note: The value of these assets will be used in future 'Net Worth' calculations, not the income forecast chart.")
        c4, c5, c6 = st.columns(3)
        with c4: st.number_input("Jewelry Value ($)", 0, None, 5000)
        with c5: st.number_input("Precious Metals Value ($)", 0, None, 10000)
        with c6: st.number_input("Guns/Heirlooms Value ($)", 0, None, 7000)

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
        df = pd.DataFrame(index=years, data={'Age': ages}); event_list = []
        
        # --- Asset Calculations (Year-over-Year) ---
        asset_cols = []
        if inc_pretax: df[pretax_name] = 0; df.loc[start_year, pretax_name] = pretax_balance; asset_cols.append(pretax_name)
        if inc_roth: df[roth_name] = 0; df.loc[start_year, roth_name] = roth_balance; asset_cols.append(roth_name)
        if inc_brokerage: df[brokerage_name] = 0; df.loc[start_year, brokerage_name] = brokerage_balance; asset_cols.append(brokerage_name)
        
        df['Investment Drawdowns'] = 0

        for i, year in enumerate(years[1:]):
            prev_year = years[i]
            age = df.loc[year, 'Age']
            
            for col in asset_cols:
                prev_balance = df.loc[prev_year, col]
                growth = prev_balance * (investment_return / 100)
                
                if age < retirement_age:
                    contrib = 0
                    if col == pretax_name: contrib = pretax_contrib * 12
                    elif col == roth_name: contrib = roth_contrib * 12
                    elif col == brokerage_name: contrib = brokerage_contrib * 12
                    df.loc[year, col] = prev_balance + growth + contrib
                else:
                    wd_rate = 0
                    if col == pretax_name: wd_rate = pretax_wd_rate / 100
                    elif col == roth_name: wd_rate = roth_wd_rate / 100
                    elif col == brokerage_name: wd_rate = brokerage_wd_rate / 100
                    
                    drawdown = (prev_balance + growth) * wd_rate
                    df.loc[year, 'Investment Drawdowns'] += drawdown
                    df.loc[year, col] = prev_balance + growth - drawdown

        # --- Income Calculations ---
        if inc_job1: # ... (income calculations are the same as before)
            job1_incomes = [(job1_income * (1 + job1_growth / 100)**i) if age < retirement_age else 0 for i, age in enumerate(ages)]; df[job1_name] = job1_incomes
            if retirement_age-1 in ages and any(v > 0 for v in job1_incomes): event_list.append({'Age': retirement_age - 1, 'Value': job1_incomes[ages.index(retirement_age-1)], 'Event': f'{job1_name} Ends', 'Source': job1_name})
        if inc_job2:
            job2_incomes = [(job2_income * (1 + job2_growth / 100)**i) if age < retirement_age else 0 for i, age in enumerate(ages)]; df[job2_name] = job2_incomes
            if retirement_age-1 in ages and any(v > 0 for v in job2_incomes): event_list.append({'Age': retirement_age - 1, 'Value': job2_incomes[ages.index(retirement_age-1)], 'Event': f'{job2_name} Ends', 'Source': job2_name})
        if inc_ss:
            df[ss_name] = [ss_annual_amount if age >= ss_start_age else 0 for age in ages]
            if ss_annual_amount > 0 and ss_start_age in ages: event_list.append({'Age': ss_start_age, 'Value': ss_annual_amount, 'Event': f'{ss_name} Begins', 'Source': ss_name})
        if inc_pension1:
            df[pension1_name] = [pension1_annual_amount if age >= pension1_start_age else 0 for age in ages]
            if pension1_annual_amount > 0 and pension1_start_age in ages: event_list.append({'Age': pension1_start_age, 'Value': pension1_annual_amount, 'Event': f'{pension1_name} Begins', 'Source': pension1_name})
        if inc_pension2:
            df[pension2_name] = [pension2_annual_amount if age >= pension2_start_age else 0 for age in ages]
            if pension2_annual_amount > 0 and pension2_start_age in ages: event_list.append({'Age': pension2_start_age, 'Value': pension2_annual_amount, 'Event': f'{pension2_name} Begins', 'Source': pension2_name})
        
        # --- Final Aggregation ---
        income_cols = [c for c in [job1_name, job2_name, ss_name, pension1_name, pension2_name, 'Investment Drawdowns'] if c in df.columns]
        df['Total Income'] = df[income_cols].sum(axis=1)
        df_melted = df.reset_index().melt(id_vars=['index', 'Age'], value_vars=income_cols + ['Total Income'], var_name='Source', value_name='Value'); df_melted.rename(columns={'index':'Year'}, inplace=True)
        
        # --- Charting ---
        st.subheader("Income Forecast")
        line_chart = alt.Chart(df_melted[df_melted['Value'] > 0]).mark_line(size=3).encode( # Filter out zero values for cleaner chart
            x=alt.X('Age:O', title='Your Age'), y=alt.Y('Value:Q', title='Annual Income', axis=alt.Axis(format='$,.0f')), color='Source:N', tooltip=['Year', 'Age', 'Source', alt.Tooltip('Value:Q', format='$,.0f')]
        ).properties(title='Annual Income Streams Over Time')
        
        if event_list:
            events_df = pd.DataFrame(event_list)
            event_markers = alt.Chart(events_df).mark_circle(size=150, stroke='white', strokeWidth=2).encode(
                x=alt.X('Age:O'), y=alt.Y('Value:Q'), color=alt.Color('Source:N'), tooltip=['Age', 'Event']
            )
            final_chart = alt.layer(line_chart, event_markers)
        else: final_chart = line_chart
        st.altair_chart(final_chart.interactive(), use_container_width=True)

        # --- Asset Growth Chart ---
        st.subheader("Asset Growth Forecast")
        assets_melted = df.reset_index().melt(id_vars=['index', 'Age'], value_vars=asset_cols, var_name='Account', value_name='Balance'); assets_melted.rename(columns={'index':'Year'}, inplace=True)
        asset_chart = alt.Chart(assets_melted).mark_area(opacity=0.8).encode(
            x=alt.X('Age:O', title='Your Age'),
            y=alt.Y('Balance:Q', title='Account Balance', axis=alt.Axis(format='$,.0f')),
            color='Account:N'
        ).properties(title="Projected Asset Growth Over Time")
        st.altair_chart(asset_chart.interactive(), use_container_width=True)

        # --- Data Tables ---
        with st.expander("View Detailed Forecast Data Table"):
            display_df = df.copy().set_index('Age')
            for col in display_df.columns: display_df[col] = display_df[col].apply(lambda x: f"${x:,.0f}")
            st.dataframe(display_df, use_container_width=True)
