from langchain_openai import OpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

load_dotenv()

llm = OpenAI(model="gpt-3.5-turbo-instruct")

prompt = PromptTemplate(
    template="Generate the catchy title for blog about {topic}",
    input_variables=["topic"]
)

topic = input("System: Enter the topic name")

chain = prompt | llm

result = chain.invoke({"topic": topic})

print(result)

