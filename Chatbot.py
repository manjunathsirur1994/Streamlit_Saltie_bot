import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

key = os.getenv('OPENAI_API_KEY')

if not key:
    st.error("API key is missing. Please set it in the .env file.")
    st.stop()

# Set up the sidebar
st.sidebar.title("Saltie")
st.sidebar.write("Cruise booking app ")

# Add an image to the sidebar
st.sidebar.image(
    r"C:\Users\ManjunathSirur\OneDrive - ZapCom Solutions Pvt. ltd\Desktop\Saltie\Streamlit_Saltie_bot\saltie2.jpg",  # Replace with the path to your image
    width=100  # Adjust the width of the image
)

st.sidebar.markdown("# LLM settings")
add_selectbox = st.sidebar.selectbox(
    'Choose the LLM you prefer',
    ('OpenAI', 'OLLAMA', 'Anthropic','Claude')
)

# Show title and description.
st.title("💬 Saltie")
st.write(
    "A platform powered by AI and analytics enabling you to positively impact employee wellness and productivity through a reward solution,  high value leisure travel offerings, community give back options and personalized shopping tools."
)

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
            "content": "You are a cruise booking chatbot with Saltie. Give all information, and don't redirect them to website."
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
