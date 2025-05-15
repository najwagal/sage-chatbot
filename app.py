import streamlit as st
from openai import OpenAI

# Set page config
st.set_page_config(page_title="SAGE - Sexual Health Support", page_icon="🧠", layout="centered")

# Custom CSS for theme
st.markdown("""
    <style>
        body {
            background-color: #f0f4f8;
        }
        .main {
            padding: 2rem;
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        footer {
            text-align: center;
            padding: 1rem;
            color: #888;
            font-size: 0.85rem;
        }
        .stChatInputContainer {
            background-color: #e8f0fe !important;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🌼 SAGE - Your Sexual Health Guide")
st.write("Welcome! I'm **SAGE**, your friendly, non-judgmental chatbot here to answer your questions about sexual health. "
         "Feel free to ask me anything — I'm here for you 💬")

# OpenAI setup
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle new user input
if prompt := st.chat_input("Ask your question here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Friendly and age-appropriate persona
        system_prompt = {
            "role": "system",
            "content": (
                "You are SAGE, a warm, empathetic chatbot who helps users ages 13+ with sexual health questions. "
                "Always respond in a clear, simple, kind, and respectful way. Avoid judgment. "
                "Use age-appropriate, inclusive language."
            )
        }

        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[system_prompt] + st.session_state.messages,
            stream=True,
        )
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})

# Footer
st.markdown("<footer>© 2025 SAGE • Designed with care for youth sexual education.</footer>", unsafe_allow_html=True)
