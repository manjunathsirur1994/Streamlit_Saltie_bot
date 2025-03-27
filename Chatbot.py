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
        [data-testid="stStatusWidget"] {display: none;}  /* Hide Running/Stop visuals */
        [data-testid="stRunningIndicator"] {display: none;}  /* Hide running indicator */
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
    st.session_state.messages = [
        {"role": "system", "content": entered_text},
        {"role": "assistant", "content": "Hello! I am Zack. Welcome to Red Rhino and Rhino's Nest, how can I help you?", "avatar": "output (1).png"}
    ]

# Define avatars
user_avatar = "output (5).png"
assistant_avatar = "output (1).png"

# Display chat history with avatars
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"], avatar=message.get("avatar", "")):
            st.markdown(message["content"])

# Display prepopulated cards after the first bot message
if len(st.session_state.messages) == 2:
    # st.write("### Quick Links")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.page_link("https://d33luei2t0ywsm.cloudfront.net/booking", label="Book a Hotel Room")
    with col2:
        st.page_link("https://www.zomato.com/bangalore/red-rhino-whitefield-bangalore/menu", label="Red Rhino Food Menu")
    with col3:
        st.page_link("https://highape.com/bangalore", label="Events Near us")
    with col4:
        st.page_link("https://www.zomato.com/bangalore/red-rhino-whitefield-bangalore", label="Book a Table at Red Rhino")

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
