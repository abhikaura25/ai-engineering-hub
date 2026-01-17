from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

### Create model object ###
embedding = OpenAIEmbeddings(model="text-embedding-3-large")

result = embedding.embed_query("Delhi is capital of India")

print(str(result))