# Import necessary libraries
from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

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
        return response.text
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")

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

    st.markdown("<div class='centered-title'>CleverQ 🤖</div>", unsafe_allow_html=True)

    st.header("Start Chat...")

    # Initialize session state variables
    if 'questions' not in st.session_state:
        st.session_state.questions = []
    if 'responses' not in st.session_state:
        st.session_state.responses = []
    if 'current_input' not in st.session_state:
        st.session_state.current_input = ""

    # Input section for current question
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    st.session_state.current_input = st.text_area(
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
        if st.session_state.current_input.strip():
            response = get_gemini_response(st.session_state.current_input)
            st.session_state.questions.insert(0, st.session_state.current_input)
            st.session_state.responses.insert(0, response)
            st.session_state.current_input = ""  # Clear input field
            st.experimental_rerun()  # Rerun to update UI
    st.markdown('</div>', unsafe_allow_html=True)

    # Display all previous questions and responses
    if st.session_state.questions:
        st.header("Question History")
        for i in range(len(st.session_state.questions)):
            st.markdown(
                f"""
                <div class="css-question-response-box">
                    <div>
                        <strong>You Asked:</strong><br>{st.session_state.questions[i]}
                    </div>
                    <div>
                        <strong>Response:</strong><br>{st.session_state.responses[i]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

# Run the main function if script is executed directly
if __name__ == "__main__":
    main()
