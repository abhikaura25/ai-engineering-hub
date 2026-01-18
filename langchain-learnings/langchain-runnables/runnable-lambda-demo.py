from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.runnables import RunnablePassthrough, RunnableParallel, RunnableLambda

load_dotenv()

model = ChatOpenAI()

def word_counter(text:str):
    return len(text.split())

runnable_word_counter = RunnableLambda(word_counter)


prompt = PromptTemplate(
    template = "write a joke about {topic}",
    input_variables=["topic"]
)


parser = StrOutputParser()

joke_generate_chain = prompt | model | parser


final_chain = joke_generate_chain | RunnableParallel(
    joke=RunnablePassthrough(),
    word_count=runnable_word_counter
)

result = final_chain.invoke({"topic": "AI"})

print(result)