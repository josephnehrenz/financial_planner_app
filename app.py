import streamlit as st
import pandas as pd
import datetime
import altair as alt
import numpy_financial as npf

# --- PAGE CONFIG ---
st.set_page_config(page_title="Future Wealth Planner", page_icon="💰", layout="wide")

# --- INITIALIZE SESSION STATE ---
if 'report_ready' not in st.session_state: st.session_state.report_ready = False
if 'expenses' not in st.session_state: st.session_state.expenses = []

def run_calculation(): st.session_state.report_ready = True
def add_expense(): st.session_state.expenses.append({'id': len(st.session_state.expenses) + 1, 'name': 'New Expense', 'type': 'Amortized Loan', 'balance': 250000, 'rate': 5.0, 'payment': 1500, 'start_age': 35})
def remove_expense(expense_id): st.session_state.expenses = [e for e in st.session_state.expenses if e['id'] != expense_id]

# --- HEADER & SIDEBAR ---
st.title("Future Wealth Planner 💰"); st.write("A comprehensive tool to forecast your financial future."); st.markdown("---")
with st.sidebar:
    st.header("Global Assumptions"); current_age = st.number_input("Your Current Age", 18, 100, 30, 1); retirement_age = st.number_input("Target Retirement Age", 40, 100, 65, 1); forecast_length = st.number_input("Forecast Length (Years)", 5, 60, 40, 1); investment_return = st.slider("Assumed Annual Investment Return (%)", 0.0, 15.0, 7.0, 0.1); inflation_rate = st.slider("Assumed Annual Inflation Rate (%)", 0.0, 5.0, 2.5, 0.1); st.markdown("---"); st.button("Calculate Financial Future", on_click=run_calculation, use_container_width=True, type="primary")

# --- TABS ---
tab_income, tab_assets, tab_expenses, tab_events, tab_report = st.tabs(["💰 Income", "📈 Assets & Investments", "💸 Expenses", "🏡 Life Events", "📊 Forecast & Report"])

with tab_income:
    st.header("Income Sources"); st.write("Detail all sources of income. Uncheck any source to exclude it from the forecast.")
    c1, c2 = st.columns(2);
    with c1: st.subheader("Primary Job"); inc_job1 = st.checkbox("Include in Forecast", True, key="inc_job1"); job1_name = st.text_input("Source Name", "Primary Job", key="job1_name"); job1_income = st.number_input("Current Annual Salary ($)", 0, None, 75000, 1000, key="job1_income"); job1_growth = st.slider("Annual Salary Growth Rate (%)", 0.0, 10.0, 3.0, 0.1, key="job1_growth")
    with c2: st.subheader("Secondary Job"); inc_job2 = st.checkbox("Include in Forecast", True, key="inc_job2"); job2_name = st.text_input("Source Name", "Side Hustle", key="job2_name"); job2_income = st.number_input("Current Annual Salary ($)", 0, None, 15000, 1000, key="job2_income"); job2_growth = st.slider("Annual Salary Growth Rate (%)", 0.0, 10.0, 2.0, 0.1, key="job2_growth")
    with st.expander("Add Future Income (Pensions, Social Security, etc.)"):
        c3, c4, c5 = st.columns(3)
        with c3: st.subheader("Social Security"); inc_ss = st.checkbox("Include in Forecast", True, key="inc_ss"); ss_name = st.text_input("Source Name", "Social Security", key="ss_name", disabled=True); ss_start_age = st.number_input("Start Age", 62, 70, 67, key="ss_start"); ss_annual_amount = st.number_input("Estimated Annual Amount ($)", 0, None, 24000, 100, key="ss_amount")
        with c4: st.subheader("Pension 1"); inc_pension1 = st.checkbox("Include in Forecast", True, key="inc_p1"); pension1_name = st.text_input("Source Name", "Military Pension", key="pension1_name"); pension1_start_age = st.number_input("Start Age", 40, 80, 55, key="p1_start"); pension1_annual_amount = st.number_input("Annual Amount ($)", 0, None, 30000, 100, key="p1_amount")
        with c5: st.subheader("Pension 2"); inc_pension2 = st.checkbox("Include in Forecast", False, key="inc_p2"); pension2_name = st.text_input("Source Name", "Corporate Pension", key="pension2_name"); pension2_start_age = st.number_input("Start Age", 40, 80, 65, key="p2_start"); pension2_annual_amount = st.number_input("Annual Amount ($)", 0, None, 12000, 100, key="p2_amount")

with tab_assets:
    st.header("Assets & Investments"); st.write("Detail your financial accounts that grow over time and can be drawn upon in retirement.")
    c1, c2, c3 = st.columns(3)
    with c1: st.subheader("Pre-Tax Retirement"); inc_pretax = st.checkbox("Include in Forecast", True, key="inc_pretax"); pretax_name = st.text_input("Account Name", "401(k)/Traditional IRA", key="pretax_name"); pretax_balance = st.number_input("Current Balance ($)", 0, None, 50000, 1000, key="pretax_bal"); pretax_contrib = st.number_input("Monthly Contribution ($)", 0, None, 500, 100, key="pretax_con"); pretax_wd_start = st.number_input("Drawdown Start Age", retirement_age, 100, retirement_age, key="pretax_wd_start"); pretax_wd_rate = st.slider("Retirement Drawdown (%/yr)", 0.0, 10.0, 4.0, 0.1, key="pretax_wd")
    with c2: st.subheader("Roth Retirement"); inc_roth = st.checkbox("Include in Forecast", True, key="inc_roth"); roth_name = st.text_input("Account Name", "Roth IRA/401(k)", key="roth_name"); roth_balance = st.number_input("Current Balance ($)", 0, None, 25000, 1000, key="roth_bal"); roth_contrib = st.number_input("Monthly Contribution ($)", 0, None, 300, 100, key="roth_con"); roth_wd_start = st.number_input("Drawdown Start Age", retirement_age, 100, retirement_age, key="roth_wd_start"); roth_wd_rate = st.slider("Retirement Drawdown (%/yr)", 0.0, 10.0, 4.0, 0.1, key="roth_wd")
    with c3: st.subheader("Taxable Brokerage"); inc_brokerage = st.checkbox("Include in Forecast", True, key="inc_brokerage"); brokerage_name = st.text_input("Account Name", "Taxable Brokerage", key="brokerage_name"); brokerage_balance = st.number_input("Current Balance ($)", 0, None, 10000, 1000, key="brokerage_bal"); brokerage_contrib = st.number_input("Monthly Contribution ($)", 0, None, 200, 100, key="brokerage_con"); brokerage_wd_start = st.number_input("Drawdown Start Age", retirement_age, 100, retirement_age, key="brokerage_wd_start"); brokerage_wd_rate = st.slider("Retirement Drawdown (%/yr)", 0.0, 10.0, 2.0, 0.1, key="brokerage_wd")
    with st.expander("Required Minimum Distributions (RMDs)"): st.info("For Pre-Tax accounts, drawdowns will be forced to begin at this age if they haven't started already."); rmd_start_age = st.number_input("RMD Start Age", 70, 80, 75, key="rmd_age")
    with st.expander("Add Physical & Other Assets"): st.caption("These assets will be used in future 'Net Worth' calculations."); c4, c5, c6 = st.columns(3);
    with c4: st.number_input("Jewelry Value ($)", 0, None, 5000);
    with c5: st.number_input("Precious Metals Value ($)", 0, None, 10000);
    with c6: st.number_input("Guns/Heirlooms Value ($)", 0, None, 7000)

with tab_expenses:
    st.header("Expenses"); st.write("Add one-time costs or recurring loans. The forecast will show your total annual expenses.")
    st.button("Add Expense", on_click=add_expense, type="primary")
    for i, expense in enumerate(st.session_state.expenses):
        st.markdown(f"---"); c1, c2, c3, c4 = st.columns([2, 2, 2, 1])
        with c1: expense['name'] = st.text_input("Expense Name", expense['name'], key=f"exp_name_{i}"); expense['type'] = st.selectbox("Expense Type", ["Amortized Loan", "One-Time Cost"], index=["Amortized Loan", "One-Time Cost"].index(expense['type']), key=f"exp_type_{i}")
        with c2: expense['balance'] = st.number_input("Total Cost / Loan Balance ($)", 0, None, expense['balance'], key=f"exp_bal_{i}"); expense['start_age'] = st.number_input("Start Age", 18, 100, expense['start_age'], key=f"exp_start_age_{i}")
        with c3:
            if expense['type'] == 'Amortized Loan': expense['rate'] = st.slider("Interest Rate (%)", 0.0, 25.0, expense['rate'], 0.1, key=f"exp_rate_{i}"); expense['payment'] = st.number_input("Monthly Payment ($)", 0, None, expense['payment'], key=f"exp_payment_{i}")
        with c4: st.write("##"); st.button("Remove", key=f"exp_remove_{i}", on_click=remove_expense, args=(expense['id'],))
        if expense['type'] == 'Amortized Loan' and expense['payment'] > 0 and expense['rate'] > 0:
            try: nper = npf.nper((expense['rate'] / 100) / 12, -expense['payment'], expense['balance']); st.metric("Estimated Years to Payoff", f"{(nper/12):.1f} years")
            except (ValueError, OverflowError): st.warning("Cannot calculate payoff with current values.")

with tab_events: st.header("Major Life Events"); st.info("Functionality for this tab will be built next.")

with tab_report:
    st.header("Your Financial Forecast")
    if not st.session_state.report_ready: st.info("Click 'Calculate Financial Future' in the sidebar to generate your forecast.")
    else:
        # --- Data Prep ---
        start_year = datetime.date.today().year; years = list(range(start_year, start_year + forecast_length + 1)); ages = list(range(current_age, current_age + forecast_length + 1))
        df = pd.DataFrame(index=years, data={'Age': ages}); event_list = []
        
        # --- Asset Calculations ---
        asset_cols, drawdown_cols = [], []
        if inc_pretax: df[pretax_name] = 0; df.loc[start_year, pretax_name] = pretax_balance; asset_cols.append(pretax_name); df[f"{pretax_name} Drawdown"] = 0; drawdown_cols.append(f"{pretax_name} Drawdown")
        if inc_roth: df[roth_name] = 0; df.loc[start_year, roth_name] = roth_balance; asset_cols.append(roth_name); df[f"{roth_name} Drawdown"] = 0; drawdown_cols.append(f"{roth_name} Drawdown")
        if inc_brokerage: df[brokerage_name] = 0; df.loc[start_year, brokerage_name] = brokerage_balance; asset_cols.append(brokerage_name); df[f"{brokerage_name} Drawdown"] = 0; drawdown_cols.append(f"{brokerage_name} Drawdown")
        for i, year in enumerate(years[1:]):
            prev_year, age = years[i], df.loc[year, 'Age']
            for col in asset_cols:
                prev_balance = df.loc[prev_year, col]; growth = prev_balance * (investment_return / 100); drawdown = 0
                if age < retirement_age:
                    contrib = {'401(k)/Traditional IRA': pretax_contrib, 'Roth IRA/401(k)': roth_contrib, 'Taxable Brokerage': brokerage_contrib}.get(col, 0) * 12
                    df.loc[year, col] = prev_balance + growth + contrib
                else:
                    wd_start, wd_rate = {'401(k)/Traditional IRA': (pretax_wd_start, pretax_wd_rate), 'Roth IRA/401(k)': (roth_wd_start, roth_wd_rate), 'Taxable Brokerage': (brokerage_wd_start, brokerage_wd_rate)}.get(col)
                    if (col == pretax_name and age >= rmd_start_age) or age >= wd_start:
                        drawdown = (prev_balance + growth) * (wd_rate / 100); df.loc[year, f"{col} Drawdown"] = drawdown
                    df.loc[year, col] = prev_balance + growth - drawdown

        # --- Income Calculations ---
        if inc_job1: job1_incomes = [(job1_income * (1 + job1_growth / 100)**i) if age < retirement_age else 0 for i, age in enumerate(ages)]; df[job1_name] = job1_incomes; event_list.append({'Age': retirement_age - 1, 'Value': job1_incomes[ages.index(retirement_age-1)], 'Event': f'{job1_name} Ends', 'Source': job1_name})
        if inc_job2: job2_incomes = [(job2_income * (1 + job2_growth / 100)**i) if age < retirement_age else 0 for i, age in enumerate(ages)]; df[job2_name] = job2_incomes; event_list.append({'Age': retirement_age - 1, 'Value': job2_incomes[ages.index(retirement_age-1)], 'Event': f'{job2_name} Ends', 'Source': job2_name})
        if inc_ss: df[ss_name] = [ss_annual_amount if age >= ss_start_age else 0 for age in ages]; event_list.append({'Age': ss_start_age, 'Value': ss_annual_amount, 'Event': f'{ss_name} Begins', 'Source': ss_name})
        if inc_pension1: df[pension1_name] = [pension1_annual_amount if age >= pension1_start_age else 0 for age in ages]; event_list.append({'Age': pension1_start_age, 'Value': pension1_annual_amount, 'Event': f'{pension1_name} Begins', 'Source': pension1_name})
        if inc_pension2: df[pension2_name] = [pension2_annual_amount if age >= pension2_start_age else 0 for age in ages]; event_list.append({'Age': pension2_start_age, 'Value': pension2_annual_amount, 'Event': f'{pension2_name} Begins', 'Source': pension2_name})
        for col in drawdown_cols:
            first_draw_year = df[df[col] > 0].first_valid_index()
            if first_draw_year: age = df.loc[first_draw_year, 'Age']; val = df.loc[first_draw_year, col]; event_list.append({'Age': age, 'Value': val, 'Event': f'{col} Begins', 'Source': col})

        # --- Expense Calculations ---
        df['Total Expenses'] = 0
        for expense in st.session_state.expenses:
            expense_name = expense['name']; df[expense_name] = 0; start_age, balance = expense['start_age'], expense['balance']
            if expense['type'] == 'One-Time Cost' and start_age in ages: df.loc[df['Age'] == start_age, expense_name] = -balance; event_list.append({'Age': start_age, 'Value': -balance, 'Event': f'{expense_name} Occurs', 'Source': 'Total Expenses'})
            elif expense['type'] == 'Amortized Loan':
                pmt, rate = expense['payment'], expense['rate']
                if pmt > 0:
                    try:
                        monthly_rate = (rate / 100) / 12 if rate > 0 else 0; nper = npf.nper(monthly_rate, -pmt, balance) if rate > 0 else balance / pmt; payoff_age = start_age + (nper / 12)
                        for age_ in range(start_age, int(payoff_age) + 1):
                            if age_ in ages: df.loc[df['Age'] == age_, expense_name] = -(pmt * 12)
                        if start_age in ages: event_list.append({'Age': start_age, 'Value': -(pmt*12), 'Event': f'{expense_name} Begins', 'Source': 'Total Expenses'})
                        if int(payoff_age) in ages: event_list.append({'Age': int(payoff_age), 'Value': df.loc[df['Age'] == int(payoff_age), expense_name].values[0], 'Event': f'{expense_name} Paid Off', 'Source': 'Total Expenses'})
                    except (ValueError, OverflowError): pass
            df['Total Expenses'] += df[expense_name]

        # --- Final Aggregation ---
        income_cols = [c for c in [job1_name, job2_name, ss_name, pension1_name, pension2_name] + drawdown_cols if c in df.columns]; df['Total Income'] = df[income_cols].sum(axis=1)
        df['Net Annual Cash Flow'] = df['Total Income'] + df['Total Expenses']
        chart_cols = income_cols + ['Total Expenses', 'Net Annual Cash Flow', 'Total Income']
        df_melted = df.reset_index().melt(id_vars=['index', 'Age'], value_vars=chart_cols, var_name='Source', value_name='Value'); df_melted.rename(columns={'index':'Year'}, inplace=True)
        
        # --- Charting (Simplified & Robust) ---
        st.subheader("Cash Flow Forecast")
        line_chart = alt.Chart(df_melted).mark_line(size=3).encode(
            x=alt.X('Age:O', title='Your Age'),
            y=alt.Y('Value:Q', title='Annual Cash Flow', axis=alt.Axis(format='$,.0f')),
            color=alt.Color('Source:N', legend=alt.Legend(title="Data Source")),
            tooltip=['Year', 'Age', 'Source', alt.Tooltip('Value:Q', format='$,.0f')]
        ).properties(title='Annual Cash Flow Over Time')
        
        if event_list:
            events_df = pd.DataFrame(event_list).dropna()
            event_markers = alt.Chart(events_df).mark_circle(size=150, stroke='white', strokeWidth=2).encode(
                x=alt.X('Age:O'), y=alt.Y('Value:Q'), color=alt.Color('Source:N'), tooltip=['Age', 'Event']
            )
            final_chart = alt.layer(line_chart, event_markers)
        else: final_chart = line_chart
        st.altair_chart(final_chart.interactive(), use_container_width=True)

        st.subheader("Asset Growth Forecast");
        assets_melted = df.reset_index().melt(id_vars=['index', 'Age'], value_vars=asset_cols, var_name='Account', value_name='Balance'); assets_melted.rename(columns={'index':'Year'}, inplace=True)
        asset_chart = alt.Chart(assets_melted).mark_area(opacity=0.8).encode(x=alt.X('Age:O', title='Your Age'), y=alt.Y('Balance:Q', title='Account Balance', axis=alt.Axis(format='$,.0f')), color='Account:N').properties(title="Projected Asset Growth Over Time")
        st.altair_chart(asset_chart.interactive(), use_container_width=True)

        with st.expander("View Detailed Forecast Data Table"):
            display_df = df.copy().set_index('Age');
            for col in display_df.columns: display_df[col] = display_df[col].apply(lambda x: f"${x:,.0f}")
            st.dataframe(display_df, use_container_width=True)
