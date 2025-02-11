import streamlit as st
import configuration

config = configuration.load_config()

# Function to update the configuration file
def update_config(key, value):
    config = configuration.load_config()
    config[key] = value
    configuration.save_config(config)
    st.success(f"{key} updated successfully! Refresh to see changes.")

st.set_page_config(layout='wide')

st.markdown("# Bot Settings")
st.write('--------------')

# ---- Change Bot Name ----
with st.container(border=True):
    st.write("### Bot Name")
    
    with st.expander("Current bot name"):
        st.write(config['chatbot_name'])

    bot_name = st.text_input("Enter the Chatbot's name to change it and save it.")
    
    if st.button("Save Name"):
        update_config("chatbot_name", bot_name)

# ---- Change Subtitle ----
with st.container(border=True):
    st.write("### Bot Subtitle")
    
    with st.expander("Current subtitle"):
        st.write(config['Subtitle'])

    sub = st.text_input("Enter the subtitle to change it and save it.")

    if st.button("Save Subtitle"):
        update_config("Subtitle", sub)

# ---- Change Prompt ----
st.markdown("# Prompt Settings")
st.write('--------------')

with st.container(border=True):
    with st.expander("Show current prompt"):
        st.write(config['Prompt'])

    text_input = st.text_input("Enter your prompt to change it.")

    if st.button("Save Prompt"):
        update_config("Prompt", text_input)
