import streamlit as st  # Streamlit library import pannuthu, UI create pannurathukku
import json  # JSON handling-ku json library
import os  # OS library, file paths and environment variables handle pannurathukku
import openai  # OpenAI library GPT-3.5 use pannurathukku
from openai import OpenAI  # OpenAI library-l irunthu specific class import pannuthu

# JSON file-l irunthu expenses load panni return pannurathukku
def load_expenses_as_json(file_name):
    if os.path.exists(file_name):  # Check pannuthu file irukka illaiya
        with open(file_name, "r") as file:  # File open panni
            return str(json.dumps(json.load(file)))  # JSON ah string aakki return pannuthu
    return json.dumps([])  # File illenna, empty JSON return pannuthu

# OpenAI's GPT-3.5 model call pannurathukku function
def call_gpt3(prompt):
    openai.api_key = os.environ['OPENAI_API_KEY']  # Environment variable-l irunthu API key get pannuthu
    client = OpenAI()  # OpenAI client create pannuthu

    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",  # GPT-3.5 model specify pannuthu
        prompt=prompt,  # User kudutha prompt pass pannuthu
        max_tokens = 1000  # Maximum number of tokens (words) specify pannuthu
    )
   
    return response.choices[0].text  # GPT-3.5 response return pannuthu
    
# JSON file-l irunthu expenses load pannurathukku
def load_expenses(file_name):
    if os.path.exists(file_name):  # Check pannuthu file irukka illaiya
        with open(file_name, "r") as file:  # File open panni
            return json.load(file)  # JSON load panni return pannuthu
    return []

# JSON file-l expenses save pannurathukku
def save_expenses(file_name, expenses):
    with open(file_name, "w") as file:  # File open panni
        json.dump(expenses, file)  # Expenses JSON file-l save pannuthu

# Main Streamlit application function
def main():
    # Session state variables initialize pannuthu
    if 'full_prompt' not in st.session_state:
        st.session_state.full_prompt = ""
    if 'gpt3_response' not in st.session_state:
        st.session_state.gpt3_response = ""

    if 'expenses_json' not in st.session_state:
        file_name = "expenses.json"
        st.session_state.expenses_json = ""

    st.title("Expense Tracker")  # Title set pannuthu UI-l

    # Load expenses
    file_name = "expenses.json"
    st.session_state.expenses_json = str(load_expenses_as_json(file_name))
    expenses = load_expenses(file_name)

    user_prompt = st.text_input("Enter your prompt for GPT-3.5")  # User prompt kudukka input field
    button = st.button("Send Data to GPT-3.5")  # Button to send data to GPT-3.5

    if button:
        full_prompt = str(st.session_state.expenses_json) + user_prompt  # Full prompt combine pannuthu
        gpt3_response = call_gpt3(full_prompt)  # GPT-3.5 call pannuthu
        st.write(gpt3_response)  # Response display pannuthu

    # New expenses add pannurathukku form
    with st.form("expense_form", clear_on_submit=True):
        date = st.date_input("Date")  # Date input field
        description = st.text_input("Description")  # Description input field
        amount = st.number_input("Amount", min_value=0.0, format="%f")  # Amount input field
        submit_button = st.form_submit_button("Add Expense")  # Submit button

        if submit_button:
            expenses.append({"date": str(date), "description": description, "amount": amount})  # New expense add pannuthu
            save_expenses(file_name, expenses)  # Save pannuthu

    # Expenses display pannurathukku
    if expenses:
        st.write("### Recorded Expenses")
        for expense in expenses:
            st.write(f"{expense['date']} - {expense['description']}: ${expense['amount']}")

    # Expenses JSON ah download panna button
    if st.button("Download Expenses as JSON"):
        with open(file_name, "r") as file:
            st.download_button(label="Download JSON", data=file, file_name="expenses.json", mime="application/json")

if __name__ == "__main__":
    main()
