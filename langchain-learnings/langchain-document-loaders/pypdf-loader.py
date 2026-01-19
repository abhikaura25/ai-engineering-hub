from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI()

parser = StrOutputParser()

script_dir = Path(__file__).parent
loader = PyPDFLoader(script_dir / 'dl-curriculum.pdf')

docs = loader.load()

prompt = PromptTemplate(
    template = "describe this {book}",
    input_variables=["book"]
)

chain = prompt | model | parser

result = chain.invoke({"topic", docs[0].page_content})

print(result)