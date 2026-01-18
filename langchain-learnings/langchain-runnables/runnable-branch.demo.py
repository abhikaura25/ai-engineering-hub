from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()
model = ChatOpenAI()
parser = StrOutputParser()

def word_counter(text: str):
    return len(text.split())

def is_long_text(text: str):
    return word_counter(text) > 250

report_generate_prompt = PromptTemplate(
    template="Generate report on the {topic}",
    input_variables=["topic"]
)

summarize_prompt = PromptTemplate(
    template="Summarize the following text in a concise manner:\n{text}",
    input_variables=["text"]
)

summarize_chain = summarize_prompt | model | parser

branch_chain = RunnableBranch(
    (lambda x: is_long_text(x), summarize_chain),
    RunnablePassthrough()
)

final_chain = report_generate_prompt | model | parser | branch_chain

result = final_chain.invoke({"topic": "cricket"})
print(result)