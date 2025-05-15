import streamlit as st
from openai import OpenAI

# Page config
st.set_page_config(
    page_title="SAGE - Sexual Health Support",
    page_icon="🧠",
    layout="centered"
)

# Custom CSS for welcoming theme + chat box styling + background + footer
st.markdown("""
    <style>
        body {
            background-color: #f0f4f8;  /* soft, calming pastel blue */
        }
        .main {
            padding: 2rem;
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            max-width: 700px;
            margin: auto;
        }
        .avatar {
            width: 80px;
            margin: 1rem auto;
            display: block;
            border-radius: 50%;
        }
        .stChatInputContainer {
            background-color: #e8f0fe !important; /* light blue input */
            border-radius: 12px !important;
        }
        footer {
            text-align: center;
            padding: 1rem;
            color: #888;
            font-size: 0.85rem;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

# Wrapper div for centered chat box and content
st.markdown('<div class="main">', unsafe_allow_html=True)

# Avatar + Title + Intro with flower emoji 🌼
st.image("https://i.imgur.com/fS7nZZz.png", caption="Hi, I'm SAGE!", use_column_width=False, width=120, class_="avatar")
st.title("🌼 SAGE - Your Sexual Health Guide")
st.write("Welcome! I'm **SAGE**, your friendly, non-judgmental chatbot here to answer your questions about sexual health. "
         "Feel free to ask me anything — I'm here for you 💬")

# OpenAI client init
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Session state initialization
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle new user prompt input
if prompt := st.chat_input("Ask your question here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
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

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("<footer>© 2025 SAGE • Designed with care for youth sexual education.</footer>", unsafe_allow_html=True)
