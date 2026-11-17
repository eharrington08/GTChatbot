# Lab 3: Chatbot page

import streamlit as st
from pydantic_ai import Agent

agent = Agent(
    "google:gemini-3.5-flash-lite",
    instructions =(
        "Your name is Game Guru. You are a semi-friendly assitant, although you are allowed to have some kick-back."
        "You are only permitted to help with work in video game software-development or any other topics in the video game field."
        "If the user tries to ask a non work-related topic correct them politely or not so politely, your choice."
        "Tell the user when you are not sure about something or if their question is not in your data set."
        "Remember all information about the user for recall later on in the chat."
        "Try your best to build off of your own ideas as well as ideas presented by the user."
        "Scarcely use super dramatic vocabulary, like a wizard giving a sidequest, but keep it mostly professional."
    ),
)

if "chat" not in st.session_state:
    st.session_state.chat = []
if "history" not in st.session_state:
    st.session_state.history = []
st.title("Game Guru Chatbot!")
for bubble in st.session_state.chat:
    with st.chat_message(bubble[0]):
        st.write(bubble[1])
prompt = st.chat_input("Ask Game Guru a question...")
if prompt:
    st.session_state.chat.append(("user", prompt))
    with st.chat_message("user"):
        st.write(prompt)
    with st.spinner("Thinking..."):
        try:
            result = agent.run_sync(prompt, message_history=st.session_state.history)
            st.session_state.chat.append(("assistant", result.output))
            st.session_state.history = result.all_messages()
            with st.chat_message("assistant"):
                st.write(result.output)
        except Exception as e:
            st.session_state.chat.append(("assistant","Something unexpected happened. Please try again."))
    prompt = ""