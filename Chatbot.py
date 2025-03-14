import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
import configuration

load_dotenv()

# Load latest configuration values
config = configuration.load_config()

st.set_page_config(layout='wide')

# Hide the hamburger menu
hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}

        </style>
        """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


st.title(f"{config['chatbot_name']}") 
st.write(config["Subtitle"])

key = os.getenv("OPENAI_API_KEY")

if not key:
    st.error("API key is missing. Please set it in the .env file.")
    st.stop()

entered_text = config["Prompt"]

client = OpenAI(api_key=key)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": entered_text}]

# Define avatars
user_avatar = "output (5).png"
assistant_avatar = "output (1).png"

# Display chat history with avatars
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"], avatar=message.get("avatar", "")):  
            st.markdown(message["content"])

if prompt := st.chat_input("Type in your queries here! "):
    user_message = {"role": "user", "content": prompt, "avatar": user_avatar}
    st.session_state.messages.append(user_message)

    with st.chat_message("user", avatar=user_avatar):
        st.markdown(prompt)

    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
        stream=True,
    )

    with st.chat_message("assistant", avatar=assistant_avatar):
        response = st.write_stream(stream)
    
    assistant_message = {"role": "assistant", "content": response, "avatar": assistant_avatar}
    st.session_state.messages.append(assistant_message)
