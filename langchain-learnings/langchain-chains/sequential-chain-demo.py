from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI()

first_prompt = PromptTemplate(
    template="Give the detailed information on this {topic}",
    input_variables=["topic"]
)

second_prompt = PromptTemplate(
    template="Give 3 point summary on {text}",
    input_variables=["text"]
)

parser = StrOutputParser()

chain = first_prompt | model | parser | second_prompt | model | parser

result = chain.invoke({"topic": "cricket"})

print(result)