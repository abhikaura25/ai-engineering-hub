from langchain_openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

##### create model object ####
model = OpenAI(model="gpt-3.5-turbo-instruct")

#### prompt ####
prompt = "What is the capital of India?"

result = model.invoke(prompt)

print(result)