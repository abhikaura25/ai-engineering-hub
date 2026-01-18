from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.runnables import RunnableSequence

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

chain = RunnableSequence(prompt, model, parser, explain_prompt, model, parser)

result = chain.invoke({"topic": "AI"})

print(result)