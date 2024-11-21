import streamlit as st
import requests

# Set page configuration
st.set_page_config(page_title="Smart Dashboard", page_icon="🚗", layout="wide")

# Sidebar (navigation placeholder)
st.sidebar.markdown("## Smart Dashboard")
st.sidebar.markdown("### Navigation")
st.sidebar.markdown("- [Home](#)")
st.sidebar.markdown("- [Dashboard](#)")
st.sidebar.markdown("- [Fault Detection](#)")
st.sidebar.markdown("- [Settings](#)")
st.sidebar.markdown("- [Help](#)")

# Main Layout
col1, col2 = st.columns([1, 2])

# Left Column - Image and Title
with col1:
    st.markdown("<h1 style='color: red; font-weight: bold;'>How can I Help You..!</h1>", unsafe_allow_html=True)
    st.image("mechanic.png", use_column_width=True)  # Make sure to have 'mechanic.png' in the same directory

# Right Column - Chat Interface
with col2:
    st.markdown(
        "<div style='background-color: #2D2D2D; padding: 10px; border-radius: 10px;'>"
        "<p style='color: white;'>Hello! How can I assist you with your vehicle maintenance today?</p>"
        "</div>",
        unsafe_allow_html=True
    )

    # Placeholder for chat messages
    chat_placeholder = st.empty()
    chat_history = []

    # Text input for user message
    user_message = st.text_input("Type your message here...", "")

    # Function to get a response from Gemini API
    def get_gemini_response(message):
        api_key = "AIzaSyDmW0k6J9iZGNUlg-ioYx6zIfbfGoccDUM"
        url = "https://api.gemini.com/v1/endpoint"  # Replace with actual Gemini API endpoint
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        payload = {
            "input": message
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json().get("response", "Sorry, I couldn't get a response. Please try again.")
        else:
            return "There was an error connecting to the service."

    # Process user message and get chatbot response
    if user_message:
        # Display user message
        chat_history.append((user_message, "user"))
        
        # Fetch bot response
        bot_response = get_gemini_response(user_message)
        chat_history.append((bot_response, "bot"))

        # Update chat history display
        with chat_placeholder.container():
            for message, sender in chat_history:
                if sender == "user":
                    st.markdown(f"<div style='text-align: right;'><p>{message}</p></div>", unsafe_allow_html=True)
                else:
                    st.markdown(
                        f"<div style='background-color: #2D2D2D; padding: 10px; border-radius: 10px;'>"
                        f"<p style='color: white;'>{message}</p>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
