from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI()

prompt = PromptTemplate(
    template="write a summary of the following poem \n {poem}",
    input_variables=["poem"]
)

parser = StrOutputParser()

script_dir = Path(__file__).parent
loader = TextLoader(script_dir / 'cricket.txt', encoding="utf-8")

docs = loader.load()

chain = prompt | model | parser

result = chain.invoke({"poem": docs[0].page_content})

print(result)
