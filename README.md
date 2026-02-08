# Future Wealth Planner 💰

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://isolate.menlosecurity.com/https://financialplannerapp-k4dhhsz9eecxcpb7n5tkb9.streamlit.app/) 

A comprehensive, interactive web application designed to forecast personal financial futures. This tool allows users to model complex scenarios involving multiple income streams, investments, and expenses to generate a detailed, professional-grade financial report.

---

## 🚀 Live Application

You can access and use the live application here:

**[https://financial-planner-app.streamlit.app](https://isolate.menlosecurity.com/https://financialplannerapp-k4dhhsz9eecxcpb7n5tkb9.streamlit.app/)**

---

## ✨ Features

This application provides a holistic view of your financial life through a powerful and intuitive interface.

### Input Modeling:
*   **Dynamic Income Streams:** Model multiple jobs with individual growth rates, plus future income like pensions and Social Security with specific start ages.
*   **Detailed Asset Management:** Track pre-tax, Roth, and taxable brokerage accounts. Set initial balances, monthly contributions, and post-retirement drawdown strategies.
*   **Automated RMDs:** Includes logic to automatically begin withdrawals from pre-tax accounts at the specified RMD age.
*   **Flexible Expense Tracking:** Dynamically add, remove, and model three types of expenses:
    *   **Amortized Loans:** (e.g., Mortgages, Car Loans) with auto-calculated payoff dates.
    *   **Constant Expenses:** (e.g., Groceries, Utilities) with defined start and end ages.
    *   **One-Time Costs:** (e.g., Down Payments, Major Purchases).

### Interactive Reporting & Visualization:
*   **Professional Cash Flow Forecast:** A beautiful, interactive Plotly chart that visualizes all income, expenses, and net cash flow over time.
    *   **Intelligent Hover:** Hover over any line to get precise data for that year.
    *   **Detailed Tooltips:** Hovering over "Total Income" reveals a complete breakdown of all contributing sources.
    *   **Event Markers:** Diamond markers appear on the chart to highlight key financial events (e.g., "Primary Job Ends," "Mortgage Paid Off"), with details available on hover.
*   **Executive Summary:** A high-level, CFP-style report that analyzes your data to provide:
    *   A qualitative **Financial Outlook** (e.g., "Excellent," "Good," "Needs Attention").
    *   Key retirement metrics like **Net Worth at Retirement** and **Income Replacement Ratio**.
    *   A detailed breakdown of your projected retirement income sources.
*   **Composition Charts:** A suite of stacked area charts to visualize the composition of your income, expenses, and assets over your lifetime.
*   **Detailed Data Table:** An expandable table showing the year-by-year forecast data for all calculated financial streams.

---

## 🛠️ Technology Stack

This application was built 100% in the cloud using a modern, open-source stack:

*   **Framework:** [Streamlit](https://streamlit.io/)
*   **Language:** [Python](https://www.python.org/)
*   **Data Manipulation:** [Pandas](https://pandas.pydata.org/)
*   **Financial Calculations:** [NumPy Financial](https://numpy.org/numpy-financial/)
*   **Charting:** [Plotly](https://plotly.com/python/) & [Altair](https://altair-viz.github.io/)
*   **Deployment:** [Streamlit Community Cloud](https://streamlit.io/cloud)

---

## 🕹️ How to Use

1.  **Navigate to the Live App:** Open the application in your web browser.
2.  **Set Global Assumptions:** Use the sidebar on the left to set your current age, target retirement age, and assumed investment returns.
3.  **Enter Your Financial Details:**
    *   Go to the **💰 Income** tab to add your jobs, pensions, and Social Security.
    *   Go to the **📈 Assets & Investments** tab to input your 401(k), Roth IRA, and other account balances and contributions.
    *   Go to the **💸 Expenses** tab to add any major loans, one-time costs, or recurring monthly expenses.
4.  **Calculate Your Future:** Click the **"Calculate Financial Future"** button in the sidebar.
5.  **View Your Report:** Navigate to the **📊 Forecast & Report** tab to see your interactive charts and personalized financial summary.

---

## 🤝 Acknowledgments

This project was developed in a collaborative process with Gemini, an advanced AI assistant. The iterative cycle of ideation, coding, debugging, and refinement was made possible through this human-AI partnership, demonstrating a powerful new paradigm for rapid application development.
