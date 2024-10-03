import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Streamlit App Title
st.title("SaaS Runway Calculator")

# Sidebar Inputs for Financial Data
st.sidebar.header("Enter your financial data")
monthly_revenue = st.sidebar.number_input("Monthly Revenue ($)", value=20000)
monthly_expenses = st.sidebar.number_input("Monthly Expenses ($)", value=15000)
current_cash = st.sidebar.number_input("Current Cash on Hand ($)", value=100000)
revenue_growth_rate = st.sidebar.slider("Revenue Growth Rate (%)", 0.0, 20.0, 5.0) / 100
expense_growth_rate = st.sidebar.slider("Expense Growth Rate (%)", 0.0, 20.0, 3.0) / 100
months = st.sidebar.slider("Time Frame (Months)", 1, 36, 12)
funding_injection = st.sidebar.number_input("Funding Injection (Optional) ($)", value=0)

# 2. Calculations
revenues = [monthly_revenue]
expenses = [monthly_expenses]
cash_remaining = [current_cash]

for month in range(1, months):
    # Increase revenue and expenses based on growth rates
    new_revenue = revenues[-1] * (1 + revenue_growth_rate)
    new_expenses = expenses[-1] * (1 + expense_growth_rate)
    
    # Calculate cash left after the month
    cash_left = cash_remaining[-1] + new_revenue - new_expenses
    
    # Add revenue, expenses, and cash remaining to lists
    revenues.append(new_revenue)
    expenses.append(new_expenses)
    cash_remaining.append(cash_left)

    # Inject funding at month 6 (optional)
    if month == 6:
        cash_remaining[-1] += funding_injection

# 3. Plot Graphs
fig, ax = plt.subplots()
months_list = np.arange(0, months)
ax.plot(months_list, cash_remaining, label="Cash Remaining", color='green')
ax.plot(months_list, revenues, label="Revenue", color='blue')
ax.plot(months_list, expenses, label="Expenses", color='red')
ax.set_title('SaaS Runway Over Time')
ax.set_xlabel('Months')
ax.set_ylabel('Dollars')
ax.legend()
ax.grid(True)

# Display the graph
st.pyplot(fig)

# 4. Actionable Advice
runway = next((i for i, cash in enumerate(cash_remaining) if cash < 0), months)
st.write(f"At the current burn rate, you have **{runway} months** of runway left.")

if runway < months:
    st.warning("Consider reducing expenses or increasing revenue to extend your runway.")
else:
    st.success("Your runway is secure for the given time frame.")
