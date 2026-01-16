from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

#### create a model ####
model = ChatOpenAI(model="gpt-4")

prompt = "Write 5 line poem on topic Cricket"

result = model.invoke(prompt)

print(result.content)

