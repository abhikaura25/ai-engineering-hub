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
        st.session_state['chat_history'].append({"role":"user","content":user_input})
        st.text(user_input)
        config = {"configurable": {"thread_id": uuid}}    
        result = chatbot.invoke({'messages': [  {"role":"user","content":user_input} ]}, config=config)
        ai_message = result['messages'][-1].content

    with st.chat_message("assistant"):
        st.session_state['chat_history'].append({"role":"assistant","content":ai_message})
        st.text(ai_message)