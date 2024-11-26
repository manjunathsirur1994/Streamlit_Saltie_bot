import streamlit as st
import matplotlib.pyplot as plt
import streamlit as st

st.markdown("# Prompts ")

default_prompt = 'You are a cruise booking chatbot with Saltie. Give all information regarding cruise booking and cruise realted only.'

try:
    with open("prompt.txt", "r") as file:
        entered_text = file.read()
        st.write(f'''Current prompt : 
                  
                 {entered_text}.

copy and paste the default prompt if needed: 
                 
                 {default_prompt}''')
except FileNotFoundError:
    st.write(f"Prompt file not found, using default prompt: {default_prompt}")


# Create a text input box with the label "Enter text"
text_input = st.text_input("Enter your prompt to change it:", "") 

# Create a save button
if st.button("Save"):
    # Access the text entered in the box
    entered_text = text_input 
    with open("prompt.txt", 'w') as file:
        file.write(entered_text)