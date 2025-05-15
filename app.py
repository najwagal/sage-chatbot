import streamlit as st
import requests

# Hugging Face setup
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-small"
HF_TOKEN = st.secrets["huggingface"]["HF_API_KEY"]
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Streamlit UI
st.set_page_config(page_title="SAGE - Sexual Health Chatbot")
st.title("SAGE – Sexual Health Chatbot")
st.write("This tool provides youth-friendly sexual health education.")

user_input = st.text_input("Ask your question:")

if user_input:
    prompt = f"""
    You are SAGE — a respectful, empathetic, and professional chatbot.
    Provide a simple, fact-based response suitable for someone aged 13.

    Question: {user_input}
    Answer:
    """
    result = query({"inputs": prompt})

    try:
        response = result[0]["generated_text"].split("Answer:")[-1].strip()
        st.markdown(f"**SAGE:** {response}")
    except Exception:
        st.error("Sorry, there was an issue processing your request.")
