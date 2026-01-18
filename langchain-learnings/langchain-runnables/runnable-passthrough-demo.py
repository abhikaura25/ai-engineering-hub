from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.runnables import RunnablePassthrough, RunnableParallel

load_dotenv()

model = ChatOpenAI()

prompt = PromptTemplate(
    template = "write a joke about {topic}",
    input_variables=["topic"]
)

explain_prompt = PromptTemplate(
    template="Explain the following joke \n {text}",
    input_variables=["text"]
)

parser = StrOutputParser()

joke_generate_chain = prompt | model | parser

explain_chain = explain_prompt | model | parser

final_chain = joke_generate_chain | RunnableParallel(
    joke=RunnablePassthrough(),
    explain_joke=explain_chain
)

result = final_chain.invoke({"topic": "AI"})

print(result)