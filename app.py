import streamlit as st
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Load secrets (if running locally with .env file)
load_dotenv()
api_key = st.secrets["general"]["OPENAI_API_KEY"]

# Initialize OpenAI LLM with API key
llm = ChatOpenAI(temperature=0.6, openai_api_key=api_key)

# Define the prompt template
prompt = PromptTemplate(
    input_variables=["user_input"],
    template="""
    You are SAGE — a warm, respectful, and judgment-free chatbot designed to answer questions about sexual health.

    Please respond to the following question in a clear, simple, and empathetic tone that a 15-year-old can understand.

    Question: {user_input}
    Answer:
    """
)

# Create the LangChain
chain = LLMChain(llm=llm, prompt=prompt)

# Set page config and style
st.set_page_config(page_title="SAGE - Sexual Health Chatbot", page_icon="🧠")

st.markdown(
    """
    <style>
    /* Background */
    .stApp {
        background: #F0F8FF;  /* Soft baby blue */
        color: #333333;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* Hide Streamlit default footer and menu */
    #MainMenu, footer {
        visibility: hidden;
    }
    /* Chat input style */
    .stTextInput>div>div>input {
        border-radius: 12px;
        padding: 10px;
        font-size: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title and intro
st.title("SAGE 🧠")
st.write("Ask me anything about sexual health. I'm here for you 💬")

# User input
user_input = st.text_input("Type your question below:")

# Chatbot response
if user_input:
    response = chain.run(user_input=user_input)
    st.markdown(f"**SAGE:** {response}")

# Friendly footer
st.markdown(
    """
    <hr style="margin-top: 2rem; margin-bottom: 0.5rem;">
    <div style="text-align: center; color: #888; font-size: 0.9rem;">
        SAGE © 2025 • Built with ❤️ using Streamlit & OpenAI<br>
        For educational use only. No judgment, just answers.
    </div>
    """,
    unsafe_allow_html=True
)
