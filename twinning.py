#!/usr/bin/env python
# coding: utf-8

# In[1]:


import google.generativeai as genai  # Import the Google Generative AI library for interacting with generative AI models
import streamlit as st  # Import the Streamlit library for building web apps
from PIL import Image  # Import the Python Imaging Library for handling image files

# Configure Streamlit app settings like title, layout, and sidebar state
st.set_page_config(
    page_title="#Twinning",  # Set the title of the page
    page_icon="👬",  # Set the icon displayed in the browser tab
    layout="centered",  # Center the content of the app
    initial_sidebar_state="collapsed",  # Start with the sidebar collapsed
)

LOGO = "twinning_logo.jpg"  # Define the path to the app's logo image
image = Image.open('twinning_logo.jpg')  # Open the logo image file

container1 = st.container(border=True)  # Create a bordered container for the welcome message

# Add content to the first container
with container1:
    # Add a centered title to the page using raw HTML
    st.markdown(
        """
        <div style='text-align:center;'>
            <h1>  Welcome to the Twinning Chatbot</h1>
        </div>
        """, unsafe_allow_html=True
    )
    # Display the logo image with optional settings for formatting
    st.image(image,
         caption="",  # No caption for the image
         clamp=False, 
         channels="RGB", 
         use_column_width=True  # Scale the image to fit the column width
    )

# Add the logo to the app's header
st.logo(
    LOGO, link=None, icon_image=None  # Display the logo without a link or alternate icon image
)

container3 = st.container(border=True)

# Add a password input box in the sidebar for users to enter their API key
with st.sidebar:
    with container3:
        api_key_input = st.sidebar.text_input(
            "Please input your Gemini API Key below and hit\n\n enter to chat.", 
            type="password")
        
# Add a button in the sidebar linking to API key instructions
with st.sidebar:
    st.link_button(
    "Don't have an API Key?",
    "https://ai.google.dev/gemini-api/docs/api-key"
    )

# Configure the generative AI library with the provided API key
genai.configure(api_key=api_key_input)

# Initialize session state variables for API key and success messages
if "api_key" not in st.session_state:
    st.session_state["api_key"] = ""  # Default API key to an empty string
if "success_message" not in st.session_state:
    st.session_state["success_message"] = False  # Default success state to False

# Validate the API key (this is placeholder logic)
if len(api_key_input) > 30:  # Check if the key is longer than 30 characters (adjust based on actual API validation rules)
    st.session_state["api_key"] = api_key_input  # Store the API key in the session state
    st.session_state["success_message"] = True  # Mark validation as successful
else:
    st.session_state["success_message"] = False  # Mark validation as failed

# Display a success message if the API key is valid
#if st.session_state["success_message"]:
    #st.success("API key accepted - your chat session is live!")

# Initialize chat history in session state if not already present
if "messages" not in st.session_state:
    st.session_state.messages = []

expander = st.expander("Disclaimer")
expander.write('''
    This is a prototype under development and may contain bugs or errors. It is intended for testing and educational purposes only. Please use this prototype with caution and at your own risk. The creator of this prototype is not responsible for any damages or losses incurred as a result of using this tool.
    '''
    )

# Create a bordered container for the chat introduction text
container = st.container(border=True)
container.write(
        """
This chatbot experience is powered by the Google Gemini LLM, which is a powerful language model designed to understand and respond to your requests in a natural and informative way. It’s like having a knowledgeable assistant at your fingertips, ready to help you with a variety of tasks.

To begin, open the panel on the left and input your Google Gemini API Key. 

** Model last updated: Sep 2024 **

        """
        )

# Display a success message if the API key is valid
if st.session_state["success_message"]:
    st.success("API key accepted - your chat session is live!")

# Create a bordered container for displaying chat messages
container2 = st.container(border=True)

# Check if chat messages exist and display them
if st.session_state.messages:
    for message in st.session_state.messages:  # Loop through each message in history
        with container2.chat_message(message["role"]):  # Display each message based on its role (user/assistant)
            st.markdown(message["content"])  # Render the content of the message
else:
    st.write("No messages in history yet.")  # Show this message if no chat history exists

# Handle user input for the chat
if prompt := st.chat_input("  💬   Ask me anything   💬  "):  # Display a chat input box
        
        st.session_state.messages.append({"role": "user", "content": prompt})  # Add the user message to chat history
        
        with st.chat_message("user"):
            st.markdown(prompt)  # Display the user message in the chat interface

        with st.chat_message("assistant"):
            message_placeholder = st.empty()  # Create an empty placeholder for the assistant's response
            
        with st.spinner("Generating response..."):  # Show a spinner while generating a response
            model = genai.GenerativeModel("gemini-1.5-flash-002")  # Initialize the generative AI model
            response = model.generate_content(prompt)  # Generate a response based on the user's input
            
            for chunk in response:  # Iterate through the response chunks
                try:
                    # Extract the text from the response structure
                    text_content = chunk.candidates[0].content.parts[0].text
                    print(text_content)  # Print the extracted text to the console (for debugging)
                except (KeyError, IndexError) as e:
                    # Handle cases where the text extraction fails
                    print("Error extracting text:", e)
                    print("_" * 80)  # Print a separator for debugging output
            
            message_placeholder.markdown(text_content)  # Update the assistant's response in the placeholder
        
        st.session_state.messages.append({"role": "assistant", "content": text_content})  # Add the assistant's response to chat history

