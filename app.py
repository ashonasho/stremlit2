import streamlit as st
import json
import os

# Function to load expenses from a JSON file
def load_expenses(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            return json.load(file)
    return []

# Function to save expenses to a JSON file
def save_expenses(file_name, expenses):
    with open(file_name, "w") as file:
        json.dump(expenses, file)

# Main Streamlit application
def main():
    st.title("Expense Tracker")

    # Load existing expenses
    file_name = "expenses.json"
    expenses = load_expenses(file_name)

    # Input form for new expenses
    with st.form("expense_form", clear_on_submit=True):
        date = st.date_input("Date")
        description = st.text_input("Description")
        amount = st.number_input("Amount", min_value=0.0, format="%f")
        submit_button = st.form_submit_button("Add Expense")

        # Add new expense to the list
        if submit_button:
            expenses.append({"date": str(date), "description": description, "amount": amount})
            save_expenses(file_name, expenses)

    # Show the expenses
    if expenses:
        st.write("### Recorded Expenses")
        for expense in expenses:
            st.write(f"{expense['date']} - {expense['description']}: ${expense['amount']}")

    # Download expenses as JSON
    if st.button("Download Expenses as JSON"):
        with open(file_name, "r") as file:
            st.download_button(label="Download JSON", data=file, file_name="expenses.json", mime="application/json")

if __name__ == "__main__":
    main()
