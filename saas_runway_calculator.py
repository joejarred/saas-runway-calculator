import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Streamlit App Title
st.title("SaaS Runway Calculator V2")

# Sidebar Inputs for Financial Data
st.sidebar.header("Enter your financial data")
monthly_revenue = st.sidebar.number_input("Monthly Revenue ($)", value=20000)
monthly_expenses = st.sidebar.number_input("Monthly Expenses ($)", value=15000)
current_cash = st.sidebar.number_input("Current Cash on Hand ($)", value=100000)
revenue_growth_rate = st.sidebar.slider("Revenue Growth Rate (%)", 0.0, 20.0, 5.0) / 100
expense_growth_rate = st.sidebar.slider("Expense Growth Rate (%)", 0.0, 20.0, 3.0) / 100
months = st.sidebar.slider("Time Frame (Months)", 1, 36, 12)
funding_injection = st.sidebar.number_input("Funding Injection (Optional) ($)", value=0)

# New Features: Pessimistic, Realistic, Optimistic Growth Scenarios
st.header("Revenue Growth Scenarios")
pessimistic_growth = st.number_input("Pessimistic Growth Rate (%)", value=5)
realistic_growth = st.number_input("Realistic Growth Rate (%)", value=15)
optimistic_growth = st.number_input("Optimistic Growth Rate (%)", value=25)

# Churn Rate Input
churn_rate = st.number_input("Churn Rate (%)", value=5)

# Burn Rate Analysis - Expense Breakdown
st.header("Burn Rate Analysis")
salaries = st.number_input("Salaries ($)", value=50000)
marketing = st.number_input("Marketing ($)", value=10000)
infrastructure = st.number_input("Infrastructure ($)", value=5000)
misc = st.number_input("Miscellaneous ($)", value=2000)

total_burn = salaries + marketing + infrastructure + misc
st.write(f"Total Monthly Burn: ${total_burn}")

# CAC and LTV Integration
st.header("Customer Acquisition Cost (CAC) and Lifetime Value (LTV)")
cac = st.number_input("CAC ($)", value=200)
ltv = st.number_input("LTV ($)", value=1000)

# Function to calculate runway based on revenue, burn rate, and growth/churn rates
def calculate_runway(revenue, burn_rate, growth_rate, churn_rate):
    months = 0
    while revenue > burn_rate:
        revenue = revenue * (1 + growth_rate / 100) * (1 - churn_rate / 100)
        months += 1
    return months

# Runway calculations for pessimistic, realistic, and optimistic scenarios
runway_pessimistic = calculate_runway(100000, total_burn, pessimistic_growth, churn_rate)
runway_realistic = calculate_runway(100000, total_burn, realistic_growth, churn_rate)
runway_optimistic = calculate_runway(100000, total_burn, optimistic_growth, churn_rate)

# Display results
st.write(f"Runway (Pessimistic): {runway_pessimistic} months")
st.write(f"Runway (Realistic): {runway_realistic} months")
st.write(f"Runway (Optimistic): {runway_optimistic} months")

# Cost Cutting Suggestions based on expenses
st.header("Cost Cutting Suggestions")

if marketing > 0:
    st.write("Consider reducing marketing spend to extend your runway.")
if infrastructure > 0:
    st.write("Reducing infrastructure costs or using cheaper alternatives can help.")
if misc > 0:
    st.write("Look into minimizing miscellaneous expenses.")

# Analysis and suggestions for CAC and LTV
profitability_ratio = ltv / cac
if profitability_ratio > 3:
    st.write("Good CAC to LTV ratio! You're in a healthy position.")
else:
    st.write("Consider improving your CAC or LTV to increase runway. Suggestions: Optimize customer retention, lower CAC via organic channels.")

# 2. Calculations for Revenue, Expenses, and Cash
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
