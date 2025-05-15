import streamlit as st
import requests

# Hugging Face API setup
API_URL = "https://api-inference.huggingface.co/models/distilgpt2"
headers = {"Authorization": f"Bearer {st.secrets['hf_token']}"}

# Function to query the model
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        st.error(f"API Error {response.status_code}: {response.text}")
        return {"error": "API call failed"}
    try:
        return response.json()
    except:
        st.error("Response could not be decoded")
        return {"error": "Invalid response format"}

# Streamlit UI
st.set_page_config(page_title="SAGE - Sexual Health Chatbot")
st.title("SAGE 🧠")
st.write("Ask me anything about sexual health. I'm here for you 💬")

user_input = st.text_input("Type your question:")

if user_input:
    prompt = f"You are SAGE, a friendly and respectful chatbot that answers questions about sexual health clearly:\n\n{user_input}"
    output = query({"inputs": prompt})

    if "error" not in output:
        st.markdown(f"**SAGE:** {output[0]['generated_text']}")
