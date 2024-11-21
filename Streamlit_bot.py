import streamlit as st 
import google.generativeai as genai

# Set page configuration
st.set_page_config(page_title="Smart Dashboard", page_icon="🚗", layout="wide")

# Configure the Gemini API
genai.configure(api_key="AIzaSyDmW0k6J9iZGNUlg-ioYx6zIfbfGoccDUM")

# Function to get a response from the Gemini API
def apnabot(prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

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

# Left Column - Title (Removed the image part)
with col1:
    st.markdown("<h1 style='color: red; font-weight: bold;'>How can I Help You..!</h1>", unsafe_allow_html=True)

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

    # Process user message and get chatbot response
    if user_message:
        # Display user message
        chat_history.append((user_message, "user"))
        
        # Fetch bot response
        bot_response = apnabot(user_message)
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
