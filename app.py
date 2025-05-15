import streamlit as st
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Load secrets (if running locally with .env file)
load_dotenv()
api_key = st.secrets["general"]["OPENAI_API_KEY"]

# Initialize OpenAI LLM
llm = ChatOpenAI(temperature=0.6)

# Define the prompt template
prompt = PromptTemplate(
    input_variables=["user_input"],
    template="""
    You are SAGE — a warm, respectful, and judgment-free chatbot designed to answer questions about sexual health.

    Please respond to the following question in a clear, simple, and empathetic tone that a 13-year-old can understand.

    Question: {user_input}
    Answer:
    """
)

# Create the LangChain
chain = LLMChain(llm=llm, prompt=prompt)

# Streamlit UI
st.set_page_config(page_title="SAGE - Sexual Health Chatbot")
st.title("SAGE 🧠")
st.write("Ask me anything about sexual health. I'm here for you 💬")

user_input = st.text_input("Type your question below:")

if user_input:
    response = chain.run(user_input=user_input)
    st.markdown(f"**SAGE:** {response}")
