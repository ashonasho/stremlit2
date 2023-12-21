import streamlit as st
import json
import os
import openai
from openai import OpenAI

# Function to load and return expenses as a JSON string
def load_expenses_as_json(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            return json.dumps(json.load(file))
    return json.dumps([])

# Function to call OpenAI's GPT-3.5
def call_gpt3(prompt):
    openai.api_key = os.environ['OPENAI_API_KEY']  # Replace with your actual API key
    client = OpenAI()

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or another GPT-3.5 model
            messages=[
                         {"role": "system", "content": "You are a helpful assistant in providing insights from expenses data given bellow in json."},
                        {"role": "user", "content": str(prompt)},
                    ],
            max_tokens=150
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return str(e)

# Main Streamlit application
# def main():
#     st.title("Expense Tracker")

#     # Load existing expenses
#     file_name = "expenses.json"
#     expenses_json = load_expenses_as_json(file_name)

#     # Rest of your existing code...

#     # Button for GPT-3.5 call
    

    

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
    if 'full_prompt' not in st.session_state:
        st.session_state.full_prompt = ""
    if 'gpt3_response' not in st.session_state:
        st.session_state.gpt3_response = "gpt3_response"

    if 'expenses_json' not in st.session_state:
        file_name = "expenses.json"
        st.session_state.expenses_json = ""
    st.title("Expense Tracker")

    # Load existing expenses
    file_name = "expenses.json"
    st.session_state.expenses_json = str(load_expenses_as_json(file_name))
    expenses = load_expenses(file_name)
    button = st.button("Send Data to GPT-3.5")
    # full_prompt=" "
    if button:
        # user_prompt = st.text_input("Enter your prompt for GPT-3.5")
        st.session_state.full_prompt = str(st.session_state.expenses_json) + "\n\n" + "what is the total expense"
        st.session_state.gpt3_response = call_gpt3(st.session_state.full_prompt)
        # print(gpt3_response)
        # if 'gpt3_response' not in st.session_state:
        # st.session_state.gpt3_response = str(gpt3_response)
        st.text_area("GPT-3.5 Response",st.session_state.gpt3_response, height=300)
    st.write(st.session_state.full_prompt)
    st.write(st.session_state.expenses_json)
    st.text_area("GPT-3.5 Resse",st.session_state.gpt3_response, height=300)



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
