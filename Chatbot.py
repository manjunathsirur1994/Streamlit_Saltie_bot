import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
import configuration
load_dotenv()

# to make default page size to wide

def wide_space_default():
    st.set_page_config(layout='wide')

wide_space_default()

key = os.getenv('OPENAI_API_KEY')

if not key:
    st.error("API key is missing. Please set it in the .env file.")
    st.stop()

entered_text = configuration.Prompt

# Set up the sidebar
st.sidebar.title("Configurations")

st.sidebar.markdown("# LLM settings")
add_selectbox = st.sidebar.selectbox(
    'Choose the LLM you prefer',
    ('gpt-4o-mini by OpenAI', 'Ollama2 by Meta', 'Anthropic','Gemini by Google')
)

# Show title and description.
st.title(f"💬 {configuration.chatbot_name}")
st.write(configuration.Subtitle)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management

# Create an OpenAI client.
client = OpenAI(api_key=key)

# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": entered_text
        }
    ]

# Display the existing chat messages via `st.chat_message`, excluding the system prompt.
for message in st.session_state.messages:
    if message["role"] != "system":  # Skip displaying the system prompt
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
if prompt := st.chat_input("Welcome to Saltie, one-stop cruise booking app"):

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate a response using the OpenAI API.
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    )

    # Stream the response to the chat using `st.write_stream`, then store it in 
    # session state.
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
