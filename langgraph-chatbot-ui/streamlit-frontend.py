import streamlit as st
from langgraph_backend import chatbot
import uuid

uuid = str(uuid.uuid4())

chat_history = []

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

user_input = st.chat_input("Type your message here...")

for message in st.session_state['chat_history']:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input:
    with st.chat_message("user"):
        st.session_state['chat_history'].append({"role": "user", "content": user_input})
        st.text(user_input)

    config = {"configurable": {"thread_id": uuid}}

    with st.chat_message("assistant"):
        full_response = st.write_stream(
            message_chunk.content for message_chunk,metadata in chatbot.stream(
                {'messages': [{"role": "user", "content": user_input}]},
                config=config,
                stream_mode="messages"
            ) 
        )
        st.session_state['chat_history'].append({"role": "assistant", "content": full_response})