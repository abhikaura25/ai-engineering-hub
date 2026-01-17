from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

chat_template = ChatPromptTemplate([
    ('system', 'Your are helpful {domain} expert'),
    ('human', 'explain in simple terms, what is {topic}')])

prompt = chat_template.invoke({'domain': 'cricket', 'topic': 'dusra'})

model = ChatOpenAI()
result = model.invoke(prompt)

print(result.content)