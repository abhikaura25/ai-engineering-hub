from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

model = ChatOpenAI()

parser = StrOutputParser()

prompt_first = PromptTemplate(
    template= """ Write a detailed report on {topic} """,
    input_variables={'topic'}
)

prompt_second = PromptTemplate(
    template= """ write 4 point summary on the following text : \n {text} """,
    input_variables={'text'}
)

chain = prompt_first | model | parser | prompt_second | model |  parser

result = chain.invoke({'topic': 'cricket'})

print(result)

chain.get_graph().print_ascii() 