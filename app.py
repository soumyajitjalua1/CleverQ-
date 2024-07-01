# Import necessary libraries
from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Configure the Google API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("API key not found. Please check your .env file.")
    st.stop()

genai.configure(api_key=api_key)

# Initialize the generative model
model = genai.GenerativeModel("gemini-pro")

# Function to get responses from the model
def get_gemini_response(input_text):
    try:
        response = model.generate_content(input_text)
        return response.candidates[0].content.parts[0].text
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        return None

# Initialize Streamlit app
st.set_page_config(page_title="Q & A with CleverQ", layout="wide", initial_sidebar_state="expanded")

# Define main function for Streamlit app
def main():
    st.markdown(
        """
        <style>
            .centered-title {
                display: flex;
                justify-content: center;
                align-items: center;
                font-size: 3em;
            }
            .sidebar .sidebar-content {
                background-color: #f0f2f6;
            }
            .css-1aumxhk {
                padding: 1rem;
                border-radius: 0.5rem;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                margin-bottom: 1rem;
            }
            .css-question-response-box {
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                margin-bottom: 10px;
            }
            .css-question-response-box > div {
                flex: 1;
                border-radius: 10px;
                padding: 10px;
                box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.1);
            }
            .css-question-response-box > div:nth-child(1) {
                background-color: #eaf6fd;
            }
            .css-question-response-box > div:nth-child(2) {
                background-color: #f9f9f9;
                margin-left: 10px;
            }
            .input-container {
                display: flex;
                justify-content: center;
                align-items: center;
                width: 100%;
                max-width: 700px;
                margin: auto;
            }
            .input-container textarea {
                height: 50px;
                width: 100%;
            }
            .input-container button {
                height: 50px;
                margin-left: 10px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.sidebar.date_input('Today\'s Date', datetime.now())
    
    # Initialize session state variables
    if 'tabs' not in st.session_state:
        st.session_state.tabs = {'Main': {'questions': [], 'responses': []}}
    if 'current_tab' not in st.session_state:
        st.session_state.current_tab = 'Main'

    # Sidebar for managing tabs
    with st.sidebar:
        st.subheader("Conversation Tabs")
        tab_names = list(st.session_state.tabs.keys())
        selected_tab = st.selectbox("Select a tab:", tab_names, index=tab_names.index(st.session_state.current_tab))
        new_tab_name = st.text_input("New tab name:")
        if st.button("Create new tab"):
            if new_tab_name and new_tab_name not in st.session_state.tabs:
                st.session_state.tabs[new_tab_name] = {'questions': [], 'responses': []}
                st.session_state.current_tab = new_tab_name
                st.experimental_rerun()

    # Update current tab based on sidebar selection
    st.session_state.current_tab = selected_tab

    st.markdown("<div class='centered-title'>CleverQ 🤖</div>", unsafe_allow_html=True)

    st.header("Start Chat...")

    # Initialize session state variables for input
    if 'current_input' not in st.session_state:
        st.session_state.current_input = ""

    # Input section for current question
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    input_question = st.text_area(
        "Input your question:", 
        value=st.session_state.current_input, 
        key="input_question", 
        height=50, 
        max_chars=300,
        placeholder="Type your question here...",
        label_visibility='collapsed'
    )

    # Submit button to generate response
    if st.button("Submit", key="submit_button"):
        if input_question.strip():
            response = get_gemini_response(input_question)
            if response:
                st.session_state.tabs[st.session_state.current_tab]['questions'].insert(0, input_question)
                st.session_state.tabs[st.session_state.current_tab]['responses'].insert(0, response)
                st.session_state.current_input = ""  # Clear input field
                st.experimental_rerun()  # Rerun to update UI
    st.markdown('</div>', unsafe_allow_html=True)

    # Display all previous questions and responses for the current tab
    current_tab_data = st.session_state.tabs[st.session_state.current_tab]
    if current_tab_data['questions']:
        st.header("Question History")
        for i in range(len(current_tab_data['questions'])):
            st.markdown(
                f"""
                <div class="css-question-response-box">
                    <div>
                        <strong>You Asked:</strong><br>{current_tab_data['questions'][i]}
                    </div>
                    <div>
                        <strong>Response:</strong><br>{current_tab_data['responses'][i]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

# Run the main function if script is executed directly
if __name__ == "__main__":
    main()
