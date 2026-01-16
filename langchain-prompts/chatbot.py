from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI()

chat_history = [
    SystemMessage(content="You are helpful AI assistant")
]

while True:
    user_input = input('YOU:')
    if user_input == 'exit':
        break
    else:
        chat_history.append(HumanMessage(content=user_input))
        result = model.invoke(chat_history)
        chat_history.append(AIMessage(content=result.content))
        print("AI:", result.content)

print(chat_history)
