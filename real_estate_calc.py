import streamlit as st
import pandas as pd


def calculate_house_cost(monthly_payment, down_payment, interest_rate, loan_term_years):
    monthly_interest_rate = interest_rate / 12
    total_payments = loan_term_years * 12
    loan_amount = monthly_payment * (1 - (1 + monthly_interest_rate)**(-total_payments)) / monthly_interest_rate
    house_cost = loan_amount + down_payment
    return house_cost

def calculate_monthly_payment(house_cost, down_payment, interest_rate, loan_term_years):
    loan_amount = house_cost - down_payment
    monthly_interest_rate = interest_rate / 12
    total_payments = loan_term_years * 12
    monthly_payment = (monthly_interest_rate * loan_amount) / (1 - (1 + monthly_interest_rate) ** (-total_payments))
    return monthly_payment

def calculate_total_interest(monthly_payment, loan_term_years, loan_amount):
    total_paid = monthly_payment * loan_term_years * 12
    total_interest = total_paid - loan_amount
    return total_interest

def run():
  # Streamlit page configuration
  st.title("Mortgage Payment Calculator")

  # Input fields
  house_cost = st.number_input("House Price (€)", min_value=0.0, value=1000000.0, step=10000.0)
  down_payment = st.number_input("Down Payment (€)", min_value=0.0, value=200000.0, step=10000.0)
  interest_rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, value=4.0, step=0.1) / 100
  loan_term_years = st.number_input("Loan Duration (Years)", min_value=1, value=30, step=1)

  # Calculate button
  if st.button("Calculate"):
      monthly_payment = calculate_monthly_payment(house_cost, down_payment, interest_rate, loan_term_years)

      # Divider
      st.markdown("---")
      interest_rates = [i / 1000 for i in range(10, 41, 1)]  # 1% to 4% in 0.1% steps

      house_prices = [calculate_house_cost(monthly_payment, down_payment, rate, loan_term_years) for rate in interest_rates]
      total_interest = [calculate_total_interest(monthly_payment, loan_term_years, house_price - down_payment) for house_price in house_prices]


      df = pd.DataFrame({
          'Interest Rate (%)': [f"{rate*100:.1f}" for rate in interest_rates],
          'Monthly Payment (€)': monthly_payment,
          'House Cost (€)': house_prices,
          'Total Interests (€)': total_interest,
      })
      df['Total Paid (€)'] = df['House Cost (€)'] + df['Total Interests (€)']
      
      st.table(df.style.format(
          {'House Cost (€)': '${:,.2f}', 
           'Monthly Payment (€)': '${:,.2f}', 
           'Total Interests (€)': '${:,.2f}',
           'Total Paid (€)': '${:,.2f}'}))


  # Run this script with: streamlit run script_name.py

if __name__ == "__main__":
    run()
