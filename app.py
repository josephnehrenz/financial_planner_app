import streamlit as st
import pandas as pd
import datetime
import altair as alt
import numpy_financial as npf
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="Future Wealth Planner", page_icon="💰", layout="wide")

# --- INITIALIZE SESSION STATE ---
if 'report_ready' not in st.session_state: st.session_state.report_ready = False
if 'expenses' not in st.session_state: st.session_state.expenses = []

# --- FUNCTIONS ---
def run_calculation(): st.session_state.report_ready = True
def add_expense(): st.session_state.expenses.append({'id': len(st.session_state.expenses) + 1, 'name': 'New Expense', 'type': 'Amortized Loan', 'balance': 250000, 'rate': 5.0, 'payment': 1500, 'start_age': 35, 'end_age': 65})
def remove_expense(expense_id): st.session_state.expenses = [e for e in st.session_state.expenses if e['id'] != expense_id]

# --- HEADER & SIDEBAR ---
st.title("Future Wealth Planner 💰"); st.write("A comprehensive tool to forecast your financial future."); st.markdown("---")
with st.sidebar:
    st.header("Global Assumptions"); current_age = st.number_input("Your Current Age", 18, 100, 30, 1); retirement_age = st.number_input("Target Retirement Age", 40, 100, 65, 1); forecast_length = st.number_input("Forecast Length (Years)", 5, 60, 40, 1); investment_return = st.slider("Assumed Annual Investment Return (%)", 0.0, 15.0, 7.0, 0.1); inflation_rate = st.slider("Assumed Annual Inflation Rate (%)", 0.0, 5.0, 2.5, 0.1); st.markdown("---"); st.button("Calculate Financial Future", on_click=run_calculation, use_container_width=True, type="primary")

# --- TABS ---
tab_income, tab_assets, tab_expenses, tab_events, tab_report = st.tabs(["💰 Income", "📈 Assets & Investments", "💸 Expenses", "🏡 Life Events", "📊 Forecast & Report"])

with tab_income:
    # ... Income tab code is unchanged ...
    st.header("Income Sources"); st.write("Detail all sources of income.")
    c1, c2 = st.columns(2);
    with c1: st.subheader("Primary Job"); inc_job1 = st.checkbox("Include in Forecast", True, key="inc_job1"); job1_name = st.text_input("Source Name", "Primary Job", key="job1_name"); job1_income = st.number_input("Current Annual Salary ($)", 0, None, 75000, 1000, key="job1_income"); job1_growth = st.slider("Annual Salary Growth Rate (%)", 0.0, 10.0, 3.0, 0.1, key="job1_growth")
    with c2: st.subheader("Secondary Job"); inc_job2 = st.checkbox("Include in Forecast", True, key="inc_job2"); job2_name = st.text_input("Source Name", "Side Hustle", key="job2_name"); job2_income = st.number_input("Current Annual Salary ($)", 0, None, 15000, 1000, key="job2_income"); job2_growth = st.slider("Annual Salary Growth Rate (%)", 0.0, 10.0, 2.0, 0.1, key="job2_growth")
    with st.expander("Add Future Income (Pensions, Social Security, etc.)"):
        c3, c4, c5 = st.columns(3)
        with c3: st.subheader("Social Security"); inc_ss = st.checkbox("Include in Forecast", True, key="inc_ss"); ss_name = st.text_input("Source Name", "Social Security", key="ss_name", disabled=True); ss_start_age = st.number_input("Start Age", 62, 70, 67, key="ss_start"); ss_annual_amount = st.number_input("Estimated Annual Amount ($)", 0, None, 24000, 100, key="ss_amount")
        with c4: st.subheader("Pension 1"); inc_pension1 = st.checkbox("Include in Forecast", True, key="inc_p1"); pension1_name = st.text_input("Source Name", "Military Pension", key="pension1_name"); pension1_start_age = st.number_input("Start Age", 40, 80, 55, key="p1_start"); pension1_annual_amount = st.number_input("Annual Amount ($)", 0, None, 30000, 100, key="p1_amount")
        with c5: st.subheader("Pension 2"); inc_pension2 = st.checkbox("Include in Forecast", False, key="inc_p2"); pension2_name = st.text_input("Source Name", "Corporate Pension", key="pension2_name"); pension2_start_age = st.number_input("Start Age", 40, 80, 65, key="p2_start"); pension2_annual_amount = st.number_input("Annual Amount ($)", 0, None, 12000, 100, key="p2_amount")

with tab_assets:
    # ... Assets tab code is unchanged ...
    st.header("Assets & Investments"); st.write("Detail your financial accounts.")
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
    st.header("Expenses"); st.write("Add one-time costs, recurring loans, or constant monthly expenses.")
    st.button("Add Expense", on_click=add_expense, type="primary")
    for i, expense in enumerate(st.session_state.expenses):
        st.markdown(f"---"); c1, c2, c3, c4 = st.columns([2, 2, 2, 1])
        with c1:
            expense['name'] = st.text_input("Expense Name", expense['name'], key=f"exp_name_{i}")
            expense['type'] = st.selectbox("Type", ["Amortized Loan", "Constant", "One-Time Cost"], index=["Amortized Loan", "Constant", "One-Time Cost"].index(expense['type']), key=f"exp_type_{i}")
        with c2:
            label = "Total Cost ($)" if expense['type'] == 'One-Time Cost' else "Loan Balance ($)" if expense['type'] == 'Amortized Loan' else "Monthly Cost ($)"
            expense['balance'] = st.number_input(label, 0, None, expense['balance'], key=f"exp_bal_{i}")
            expense['start_age'] = st.number_input("Start Age", 18, 100, expense['start_age'], key=f"exp_start_age_{i}")
        with c3:
            if expense['type'] == 'Amortized Loan':
                expense['rate'] = st.slider("Interest Rate (%)", 0.0, 25.0, expense['rate'], 0.1, key=f"exp_rate_{i}")
                expense['payment'] = st.number_input("Monthly Payment ($)", 0, None, expense['payment'], key=f"exp_payment_{i}")
            elif expense['type'] == 'Constant':
                expense['end_age'] = st.number_input("End Age", expense['start_age'], 120, expense['end_age'], key=f"exp_end_age_{i}")
        with c4: st.write("##"); st.button("Remove", key=f"exp_remove_{i}", on_click=remove_expense, args=(expense['id'],))
        if expense['type'] == 'Amortized Loan' and expense.get('payment', 0) > 0 and expense.get('rate', 0) > 0:
            try: nper = npf.nper((expense['rate'] / 100) / 12, -expense['payment'], expense['balance']); st.metric("Estimated Years to Payoff", f"{(nper/12):.1f} years")
            except (ValueError, OverflowError): st.warning("Cannot calculate payoff.")

with tab_events: st.header("Major Life Events"); st.info("Functionality for this tab is in development.")

with tab_report:
    st.header("Your Financial Forecast")
    if not st.session_state.report_ready: st.info("Click 'Calculate Financial Future' in the sidebar to generate your forecast.")
    else:
        # --- Data Prep ---
        start_year = datetime.date.today().year; years = list(range(start_year, start_year + forecast_length + 1)); ages = list(range(current_age, current_age + forecast_length + 1))
        df = pd.DataFrame(index=years, data={'Age': ages})
        
        # ... (Asset & Income calculations are unchanged) ...
        asset_cols, drawdown_cols = [], [];
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
        if inc_job1: df[job1_name] = [(job1_income * (1 + job1_growth / 100)**i) if age < retirement_age else 0 for i, age in enumerate(ages)]
        if inc_job2: df[job2_name] = [(job2_income * (1 + job2_growth / 100)**i) if age < retirement_age else 0 for i, age in enumerate(ages)]
        if inc_ss: df[ss_name] = [ss_annual_amount if age >= ss_start_age else 0 for age in ages]
        if inc_pension1: df[pension1_name] = [pension1_annual_amount if age >= pension1_start_age else 0 for age in ages]
        if inc_pension2: df[pension2_name] = [pension2_annual_amount if age >= pension2_start_age else 0 for age in ages]

        # --- Expense Calculations ---
        expense_cols = []; df['Total Expenses'] = 0
        for expense in st.session_state.expenses:
            name, type, start_age, balance = expense['name'], expense['type'], expense['start_age'], expense['balance']
            df[name] = 0; expense_cols.append(name)
            if type == 'One-Time Cost' and start_age in ages: df.loc[df['Age'] == start_age, name] = -balance
            elif type == 'Constant' and start_age in ages: end_age = expense.get('end_age', 120); df.loc[(df['Age'] >= start_age) & (df['Age'] < end_age), name] = -(balance * 12)
            elif type == 'Amortized Loan':
                pmt, rate = expense.get('payment', 0), expense.get('rate', 0)
                if pmt > 0:
                    try:
                        monthly_rate = (rate / 100) / 12 if rate > 0 else 0; nper = npf.nper(monthly_rate, -pmt, balance) if rate > 0 else balance / pmt; payoff_age = start_age + (nper / 12)
                        for age_ in range(start_age, int(payoff_age) + 1):
                            if age_ in ages: df.loc[df['Age'] == age_, name] = -(pmt * 12)
                    except (ValueError, OverflowError): pass
            df['Total Expenses'] += df[name]

        # --- Final Aggregation ---
        income_cols = [c for c in [job1_name, job2_name, ss_name, pension1_name, pension2_name] + drawdown_cols if c in df.columns]; df['Total Income'] = df[income_cols].sum(axis=1)
        df['Net Annual Cash Flow'] = df['Total Income'] + df['Total Expenses']
        
        # --- Create Hover Data for Plotly ---
        df['hover_text'] = df[income_cols].apply(lambda row: '<br>'.join([f"{col}: ${val:,.0f}" for col, val in row.items() if val > 0]), axis=1)

        # --- PLOTLY CASH FLOW CHART ---
        st.subheader("Interactive Cash Flow Forecast")
        chart_cols = income_cols + ['Total Expenses', 'Net Annual Cash Flow', 'Total Income']
        df_melted = df.reset_index().melt(id_vars=['index', 'Age', 'hover_text'], value_vars=chart_cols, var_name='Source', value_name='Value'); df_melted.rename(columns={'index':'Year'}, inplace=True)
        
        fig = px.line(df_melted, x="Age", y="Value", color='Source', custom_data=['hover_text'])
        fig.update_layout(title="Annual Cash Flow Over Time", xaxis_title="Your Age", yaxis_title="Annual Cash Flow", yaxis_tickformat='$,.0f')
        fig.update_traces(
            hovertemplate="<br>".join([
                "<b>Age: %{x}</b>",
                "Source: %{fullData.name}",
                "Amount: %{y:$,.0f}",
                "<br><b>Total Income Breakdown:</b><br>%{customdata[0]}",
            ])
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # --- CFP-STYLE REPORT ---
        st.markdown("---")
        st.subheader("Executive Summary")
        ret_income_avg = df[df['Age'] >= retirement_age]['Total Income'].mean()
        pre_ret_income_avg = df[(df['Age'] >= retirement_age - 5) & (df['Age'] < retirement_age)]['Total Income'].mean()
        replacement_ratio = (ret_income_avg / pre_ret_income_avg) * 100 if pre_ret_income_avg > 0 else 0
        net_worth_at_retirement = df.loc[df['Age'] == retirement_age, asset_cols].sum().sum()
        
        summary_color = "green" if replacement_ratio >= 70 else "orange" if replacement_ratio >= 50 else "red"
        st.markdown(f"### <span style='color:{summary_color};'>Your Financial Outlook is {summary_color.capitalize()}</span>", unsafe_allow_html=True)
        if summary_color == 'green': st.write("Your current plan puts you on a solid trajectory. Your projected retirement income comfortably replaces a significant portion of your working income.")
        elif summary_color == 'orange': st.write("Your plan is on a cautionary path, replacing a moderate portion of your income. Consider increasing savings or adjusting retirement expectations.")
        else: st.write("Your plan requires attention. Your projected retirement income is low compared to your working income. It is highly recommended to review savings rates, investment choices, or retirement timing.")

        st.markdown("---")
        st.subheader("Retirement Snapshot")
        c1, c2, c3 = st.columns(3)
        c1.metric("Projected Net Worth at Retirement", f"${net_worth_at_retirement:,.0f}")
        c2.metric("Avg. Annual Retirement Income", f"${ret_income_avg:,.0f}")
        c3.metric("Income Replacement Ratio", f"{replacement_ratio:.0f}%")
        
        ret_income_sources = df[df['Age'] >= retirement_age][income_cols].mean()
        ret_income_sources = ret_income_sources[ret_income_sources > 0]
        if not ret_income_sources.empty:
            st.write("**Average Retirement Income Breakdown:**")
            st.dataframe(ret_income_sources.apply(lambda x: f"${x:,.0f} ({x/ret_income_sources.sum()*100:.0f}%)"), use_container_width=True)

        st.markdown("---")
        st.subheader("Asset & Expense Analysis")
        c1, c2 = st.columns(2)
        with c1:
            st.write("**Asset Summary**")
            total_assets_end = df[asset_cols].iloc[-1].sum()
            st.write(f"Your investment portfolio is projected to grow to **${total_assets_end:,.0f}** by the end of the forecast period.")
        with c2:
            st.write("**Expense Summary**")
            total_expenses = df[expense_cols].sum().sum()
            st.write(f"You are projected to pay a total of **${-total_expenses:,.0f}** towards your major expenses over the forecast period.")

        # --- Other Charts & Data Table ---
        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Expense Forecast");
            expense_melted = df.reset_index().melt(id_vars=['index', 'Age'], value_vars=expense_cols, var_name='Expense', value_name='Cost'); expense_melted['Cost'] = -expense_melted['Cost']
            expense_chart = alt.Chart(expense_melted[expense_melted['Cost'] > 0]).mark_area(opacity=0.8).encode(x=alt.X('Age:O', title='Your Age'), y=alt.Y('Cost:Q', title='Annual Cost', axis=alt.Axis(format='$,.0f')), color='Expense:N').properties(title="Projected Annual Expenses")
            st.altair_chart(expense_chart.interactive(), use_container_width=True)
        with c2:
            st.subheader("Asset Growth Forecast");
            assets_melted = df.reset_index().melt(id_vars=['index', 'Age'], value_vars=asset_cols, var_name='Account', value_name='Balance');
            asset_chart = alt.Chart(assets_melted).mark_area(opacity=0.8).encode(x=alt.X('Age:O', title='Your Age'), y=alt.Y('Balance:Q', title='Account Balance', axis=alt.Axis(format='$,.0f')), color='Account:N').properties(title="Projected Asset Growth Over Time")
            st.altair_chart(asset_chart.interactive(), use_container_width=True)

        with st.expander("View Detailed Forecast Data Table"):
            display_df = df.copy().set_index('Age');
            for col in display_df.columns:
                if col not in ['Age', 'cash_flow_change', 'hover_text']: display_df[col] = display_df[col].apply(lambda x: f"${x:,.0f}")
            st.dataframe(display_df.drop(columns=['hover_text']), use_container_width=True)
