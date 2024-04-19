import streamlit as st
import requests

# Define your chatbot logic function here (using Gemini API calls)
def generate_chatbot_response(user_input, api_key, endpoint_url):
    headers = {"Authorization": f"Bearer {api_key}"}
    data = {"inputs": user_input}
    response = requests.post(endpoint_url, headers=headers, json=data)

    # Process response and return chatbot's output
    return response.json()["generated_text"]

# Define chat elements
st.title("Chat with Gemini")
user_input = st.text_input("Enter your message:")

if user_input:
    chatbot_response = generate_chatbot_response(user_input,"AIzaSyA9sMh2EJfFYZt_MXLtz9rEzQcgEkC7nV0","https://api.google.com/gemini/v1/generateText")  # Call your chatbot logic function
    st.write("Chatbot:", chatbot_response)
