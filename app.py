import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="SAGE - Sexual Health Chatbot")
st.title("SAGE 🧠")
st.write("Ask me anything about sexual health. I'm here for you 💬")

# Initialize OpenAI client with secret API key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Session state to store messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask your question here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are SAGE, a warm, respectful, and judgment-free sexual health chatbot."},
                *st.session_state.messages
            ],
            stream=True
        )
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})
