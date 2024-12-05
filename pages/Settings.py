import streamlit as st
import matplotlib.pyplot as plt
import streamlit as st
import configuration

# -------------------

def wide_space_default():
    st.set_page_config(layout='wide')

wide_space_default()

# -------------------

st.markdown("# Bot Name")
st.write(f"Current Bot Name: {configuration.chatbot_name}")
bot_name = st.text_input('''Enter the Chatbot's name to change it and save it.''')

# Create a save button
if st.button("Save Name"):
    # Access the text entered in the box
    configuration.chatbot_name = bot_name 

# -------------------------

st.write(f"You can change the subtitle of the chatbot here: ")
sub = st.text_input('''Enter the subtitle to change it and save it.''')

# Create a save button
if st.button("Save subtitle"):
    # Access the text entered in the box
    configuration.Subtitle = sub 

# ---------------------------

st.markdown("# Prompts ")

default_prompt = configuration.Prompt

# Create a text input box with the label "Enter text"
text_input = st.text_input('''Enter your prompt to change it.''') 

# Create a save button
if st.button("Save Prompt"):
    configuration.Prompt = text_input
