from langgraph.graph import StateGraph,START, END
from langchain_openai import ChatOpenAI
from typing import TypedDict, Literal, Annotated
from langchain_core.messages import SystemMessage, HumanMessage,BaseMessage, AIMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
import uuid
from dotenv import load_dotenv
import sqlite3

load_dotenv()

llm = ChatOpenAI()
uuid = str(uuid.uuid4())

### Define the state structure
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]



###### Define the chat node
def chat_node(state: ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {'messages': [response]}

###### Build the state graph

graph = StateGraph(ChatState)
graph.add_node("chat", chat_node)
graph.add_edge(START, "chat")
graph.add_edge("chat", END)

conn = sqlite3.connect('chatbot.db', check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)
chatbot = graph.compile(checkpointer=checkpointer)

def retrieve_all_thread_ids():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])
    return list(all_threads)
