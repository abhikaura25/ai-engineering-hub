from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI()

parser = StrOutputParser()

template = PromptTemplate(
    template="Give 5 facts about the {topic}",
    input_variables=["topic"]
)

chain = template | model | parser

result = chain.invoke({"topic": "cricket"})

print(result)
