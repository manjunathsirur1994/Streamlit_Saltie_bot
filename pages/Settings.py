import streamlit as st
import matplotlib.pyplot as plt
import streamlit as st
import configuration

# -------------------

def wide_space_default():
    st.set_page_config(layout='wide')

wide_space_default()

# -------------------

st.markdown("# Bot Settings")
st.write('--------------')


with st.container(border=True):
    st.write(f"### Bot Name")

    with st.expander('Current bot name'):
        st.write(configuration.chatbot_name)

    bot_name = st.text_input('''Enter the Chatbot's name to change it and save it.''')

    # Create a save button
    if st.button("Save Name"):
        # Access the text entered in the box
        configuration.chatbot_name = bot_name 

# -------------------------

with st.container(border=True):
    st.write(f"### Bot Subtitle")

    with st.expander('current subtitle'):
        st.write(configuration.Subtitle)

    st.write(f"You can change the subtitle of the chatbot here: ")

    sub = st.text_input('''Enter the subtitle to change it and save it.''')

    # Create a save button
    if st.button("Save subtitle"):
        # Access the text entered in the box
        configuration.Subtitle = sub 

# ---------------------------

st.markdown("# Prompt Settings ")
st.write('--------------')

with st.container(border=True):
    default_prompt = configuration.Prompt

    with st.expander('Show current prompt'):
        st.write(f'{configuration.Prompt}')

    # Create a text input box with the label "Enter text"
    text_input = st.text_input('''Enter your prompt to change it.''') 

    # Create a save button
    if st.button("Save Prompt"):
        configuration.Prompt = text_input
