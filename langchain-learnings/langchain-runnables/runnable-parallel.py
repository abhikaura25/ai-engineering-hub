from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnableSequence
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI()
parser = StrOutputParser()

tweet_prompt = PromptTemplate(
    template="Generate Tweet about {topic}",
    input_variables=["topic"]
)

linkedin_post_prompt = PromptTemplate(
    template = "Generate a detailed linked in post about {topic}",
    input_variables=["topic"]
)

merge_prompt = PromptTemplate(
    template= "Merge the following provided tweet and linkedin post \n {tweet} \n {post}",
    input_variables=["tweet", "post"]
)

tweet_chain = tweet_prompt | model | parser
linkedin_chain = linkedin_post_prompt | model | parser

final_parallel_chain = RunnableParallel(tweet=tweet_chain, post=linkedin_chain)

result = final_parallel_chain.invoke({"topic": "AI"})

print(result)

