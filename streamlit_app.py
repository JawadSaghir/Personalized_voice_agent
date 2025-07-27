import streamlit as st
from utils.model import llm
import base64, asyncio
from main import Agent_cycle
from hugchat import hugchat
from hugchat.login import Login
import asyncio 

st.set_page_config(page_title="Scorpio",layout="wide")
with open("D:/Personalized_voice_agent/Data/Scorpio (3).png", "rb") as img_file:
    img_bytes = img_file.read()
    img_base64=base64.b64encode(img_bytes).decode()

# Embed image in HTML using base64
st.markdown(
    f"""
    <div style="display: flex; justify-content: center;">
        <img src="data:image/png;base64,{img_base64}" width="250"/>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Session state for multi-chat ---
if "conversations" not in st.session_state:
    st.session_state.conversations = []  # List of {"title": str, "messages": [(role, content)]}
if "active_conversation" not in st.session_state:
    st.session_state.active_conversation = None

# --- Sidebar: Conversation titles ---
with st.sidebar:
    st.title('History')
    for idx, conv in enumerate(st.session_state.conversations):
        if st.button(conv["title"], key=f"sidebar_conv_{idx}"):
            st.session_state.active_conversation = idx
    if st.button("New Chat"):
        st.session_state.conversations.append({"title": "New Chat", "messages": []})
        st.session_state.active_conversation = len(st.session_state.conversations) - 1
    # (Optional) Add login fields here if needed
    # if ('EMAIL' in st.secrets) and ('PASS' in st.secrets):
    #     st.success('HuggingFace Login credentials already provided!', icon='✅')
    # hf_email = st.text_input('Enter E-mail:', type='password')
    # hf_pass = st.text_input('Enter password:', type='password')
    # if not (hf_email and hf_pass):
    #     st.warning('Please enter your credentials!', icon='⚠️')
    # else:
    #     st.success('Proceed to entering your prompt message!', icon='👉')

# --- Main chat area ---
if st.session_state.active_conversation is not None:
    conversation = st.session_state.conversations[st.session_state.active_conversation]
    # Show messages
    for role, content in conversation["messages"]:
        if role == "user":
            with st.chat_message(role, avatar="D:/Personalized_voice_agent/Data/Purple Pink Gradient Man 3D Avatar.png"):
                st.markdown(content)
        else:
            with st.chat_message(role, avatar="D:/Personalized_voice_agent/Data/Colorful Gradient Girl Hijab 3D Avatar.png"):
                st.markdown(content)
    # Input
    prompt = st.chat_input("Type your message...")
    if prompt:
        # Set title if it's the first message
        if conversation["title"] == "New Chat":
            conversation["title"] = prompt[:30] + ("..." if len(prompt) > 30 else "")
        conversation["messages"].append(("user", prompt))
        with st.chat_message("user", avatar="D:/Personalized_voice_agent/Data/Purple Pink Gradient Man 3D Avatar.png"):
            st.markdown(prompt)
        with st.spinner("Thinking..."):
            reply = asyncio.run(Agent_cycle(prompt))
        conversation["messages"].append(("assistant", reply))
        with st.chat_message("assistant", avatar="D:/Personalized_voice_agent/Data/Colorful Gradient Girl Hijab 3D Avatar.png"):
            st.markdown(reply)
            try:
                for count in range(1, 20):
                    st.image(f"page_{count}.png")
            except:
                pass
            try:
                st.image("image.jpg")
            except:
                pass
else:
    st.write("Start a new chat from the sidebar.") 