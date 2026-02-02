import streamlit as st
from langgraph_backend_sqlite import chatbot, retrieve_all_thread_ids
from langchain_core.messages import HumanMessage, AIMessage
import uuid

#************** Generate Unique Thread ID for each session ****************#
def generate_uuid():
    return str(uuid.uuid4())

def reset_chat():
    st.session_state['thread_id'] = generate_uuid()
    add_thread(st.session_state['thread_id'])
    st.session_state['chat_history'] = []

def add_thread(thread_id: str):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def get_chat_history(thread_id: str):
    state = chatbot.get_state({'configurable': {'thread_id': thread_id}})
    if state.values and 'messages' in state.values:
        return state.values['messages']
    return []
    

#*********************************Session Setup *********************************#
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_uuid()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_thread_ids()

add_thread(st.session_state['thread_id'])

#***********************Side Bar UI Elements *****************************#

st.sidebar.title("Abhishek Chatbot")
st.sidebar.button("New Chat", on_click = reset_chat)
st.sidebar.header("My Conversation")

for thread in st.session_state['chat_threads'][::-1]:
    result = get_chat_history(thread) # Preload chat history for the thread
    button_label = result[0].content if result else "Start Conversation"
    if st.sidebar.button(button_label, key=thread):
        st.session_state['thread_id'] = thread
        messages = result
        temp_messages = []
        for message in messages:
            if isinstance(message, HumanMessage):
                role = "user"
            else:
                role = "assistant"
            temp_messages.append({"role": role, "content": message.content})
            
        st.session_state['chat_history'] = temp_messages

#**************************Main Chat UI Elements *****************************
user_input = st.chat_input("Type your message here...")

for message in st.session_state['chat_history']:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input:
    with st.chat_message("user"):
        st.session_state['chat_history'].append({"role": "user", "content": user_input})
        st.text(user_input)

    config = {"configurable": {"thread_id": st.session_state['thread_id']}}

    with st.chat_message("assistant"):
        full_response = st.write_stream(
            message_chunk.content for message_chunk,metadata in chatbot.stream(
                {'messages': [{"role": "user", "content": user_input}]},
                config=config,
                stream_mode="messages"
            ) 
        )
        st.session_state['chat_history'].append({"role": "assistant", "content": full_response})