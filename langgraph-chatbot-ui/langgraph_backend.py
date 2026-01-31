from langgraph.graph import StateGraph,START, END
from langchain_openai import ChatOpenAI
from typing import TypedDict, Literal, Annotated
from langchain_core.messages import SystemMessage, HumanMessage,BaseMessage, AIMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
import uuid
from dotenv import load_dotenv

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

checkpointer = InMemorySaver()
chatbot = graph.compile(checkpointer=checkpointer)

