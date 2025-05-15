import streamlit as st
from openai import OpenAI

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
            margin-top: 2rem;
        }
        .stChatInputContainer {
            background-color: #e8f0fe !important;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar content
with st.sidebar:
    st.markdown("## 🧠 About SAGE")
    st.write(
        "I'm SAGE - your **Sexual Awareness & Guidance Expert**. "
        "I'm here to provide a safe, kind, and judgment-free space for learning about sexual health. "
        "Ask me anything — no question is too weird or embarrassing. 💬"
    )

    st.markdown("---")
    st.markdown("### 🔍 Common Topics")
    st.write(
        "- Sex & Consent\n"
        "- STIs & Protection\n"
        "- Birth Control\n"
        "- Puberty & Body Changes\n"
        "- LGBTQ+ Questions\n"
        "- Emotions & Relationships"
    )

    st.markdown("---")
    st.markdown("### ⚠️ Disclaimer")
    st.write(
        "SAGE is for educational purposes only. For medical emergencies, please consult a healthcare professional or reach out to a trusted adult."
    )

    st.markdown("---")
    st.markdown("### 🛠️ Version")
    st.write("v1.0 – Beta")

# Title
st.title("SAGE - Your Sexual Health Guide 😊")
st.write("Hi, I'm **SAGE**! Feel free to ask me anything about sexual health — no question is too weird or embarrassing. 💬")

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
                "You are SAGE, a trusted older sibling or adult who helps teens aged 13+ understand sexual health. "
                "You do **not** encourage sex. You always remind that sex is for adults and focus on safety, emotions, and consent. "
                "Keep answers **short**, **clear**, and **non-judgmental**. Avoid slang, medical jargon, or adult content. "
                "Always be kind, supportive, and protective — like someone they can trust."
                "Always ask questions. Be empathetic and make them feel safe coming to you."
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
st.markdown("<footer>© 2025 SAGE Tech • Designed with care for youth.</footer>", unsafe_allow_html=True)
