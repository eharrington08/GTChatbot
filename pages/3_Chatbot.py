# Lab 3: Chatbot page
# TODO: Rename this file to fit your page. Keep the number at the front.
#
# A chatbot built with Pydantic AI (see the Pydantic AI pages on Canvas).
# It should:
#   - use a Pydantic AI Agent with instructions that fit your project's theme (no tools yet)
#   - use Streamlit's chat elements: st.chat_message and st.chat_input
#   - remember the conversation (message_history, saved in st.session_state)
#   - use try/except so an error shows a message instead of crashing the page
#   - stay on theme, without using any API or external data
#
# Your Gemini API key goes in .streamlit/secrets.toml as GOOGLE_API_KEY.

import streamlit as st
from pydantic_ai import Agent

agent = Agent(
    "google-cloud:gemini-3.5-flash-lite",
    
    instructions =(
        "You are a semi-friendly assitant, although you are allowed to have some kick-back."
        "You are only permitted to help with work-related topics."
        "If the user tries to ask a non work-related topic correct them politely or not so politely, your choice."
        "I want you to speak like tsundere."
        "Tell the user when you are not sure about something or if their question is not in your data set."
    ),
    
)

result = agent.run_sync("What can you help me with?")
st.write(result.output)
