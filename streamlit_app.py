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


# Initialize history
if "history" not in st.session_state:
    st.session_state.history = []

# Display past messages
for role, content in st.session_state.history:
    if role=="user":
        with st.chat_message(role,avatar="D:\Personalized_voice_agent\Data\Purple Pink Gradient Man 3D Avatar.png"):
            st.markdown(content)
    else:
        with st.chat_message(role,avatar="D:\Personalized_voice_agent\Data\Colorful Gradient Girl Hijab 3D Avatar.png"):
            st.markdown(content)


# In your main code, replace the streaming section with:


prompt= st.chat_input("Type your message...",)
if prompt:
        st.session_state.history.append(("user", prompt))
        with st.chat_message("user",avatar="D:\Personalized_voice_agent\Data\Purple Pink Gradient Man 3D Avatar.png"):
            st.markdown(prompt)
        

        with st.spinner("Thinking..."):

            reply=asyncio.run(Agent_cycle(prompt))

        st.session_state.history.append(("assistant", reply))
        with st.chat_message("assistant",avatar="D:\Personalized_voice_agent\Data\Colorful Gradient Girl Hijab 3D Avatar.png"):
            st.markdown(reply)
            try:
                for count in range(1,20):
                    st.image(f"page_{count}.png")

            except:
                pass
            try:
                st.image("image.jpg")
            except:
                pass
st.markdown("""
    <style>
    .fixed-bottom-bar {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100vw;
        background: #22232b;
        padding: 12px 16px 10px 16px;
        z-index: 9999;
        box-shadow: 0 -2px 8px rgba(0,0,0,0.1);
    }
    </style>
    <div class="fixed-bottom-bar"></div>
""", unsafe_allow_html=True)
st.markdown('<div class="fixed-bottom-bar">', unsafe_allow_html=True)
st.write('\n' * 2000) 
img_col, search_col, voice_col = st.columns([6, 1, 1])

with img_col:
    st.button("Image")
with search_col:
    st.button("Search")
with voice_col:
    st.button("Voice")



# Message input
        
with st.sidebar:
    st.title('Scorpio')
    # if ('EMAIL' in st.secrets) and ('PASS' in st.secrets):
    #     st.success('HuggingFace Login credentials already provided!', icon='✅')
    hf_email = st.text_input('Enter E-mail:', type='password')
    hf_pass = st.text_input('Enter password:', type='password')
    if not (hf_email and hf_pass):
        st.warning('Please enter your credentials!', icon='⚠️')
    else:
        st.success('Proceed to entering your prompt message!', icon='👉')
    