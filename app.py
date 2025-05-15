import streamlit as st
import requests

# Hugging Face API
API_URL = "https://api-inference.huggingface.co/models/distilgpt2"
headers = {"Authorization": f"Bearer {st.secrets['hf_token']}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Streamlit UI
st.title("SAGE 🧠")
st.write("Ask me anything about sexual health (powered by Hugging Face 💬)")

user_input = st.text_input("Type your question:")

if user_input:
    with st.spinner("Thinking..."):
        output = query({"inputs": user_input})
        
        # Handle potential errors
        if isinstance(output, dict) and "error" in output:
            st.error(f"Model error: {output['error']}")
        elif isinstance(output, list):
            text = output[0]["generated_text"]
            st.success(f"**SAGE:** {text}")
        else:
            st.error("Unexpected response format.")
