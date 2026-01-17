from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_core.runnables import RunnableBranch, RunnableLambda
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Literal

load_dotenv()

model = ChatOpenAI()

class Feedback(BaseModel):
    sentiment: Literal["positive", "negative"] = Field(description="Give the sentiment of the feedback")

str_parser = StrOutputParser()
pydantic_parser = PydanticOutputParser(pydantic_object=Feedback)

sentiment_prompt = PromptTemplate(
    template="Classify the sentiment of the feedback into positive, negative or neutral {feedback} \n {format_instructions}",
    input_variables=["feedback"],
    partial_variables={"format_instructions": pydantic_parser.get_format_instructions()}
)

classifier_chain = sentiment_prompt | model | pydantic_parser

positive_prompt_reply = PromptTemplate(
    template = "Write an appropriate response to this positive feedback \n {feedback}",
    input_variables=["feedback"]
)

negative_prompt_reply = PromptTemplate(
    template = "Write an appropriate response to this negative feedback \n {feedback}",
    input_variables= ["feedback"]
)

branch_chain = RunnableBranch(
    (lambda x: x.sentiment == 'positive', positive_prompt_reply| model | str_parser),
    (lambda x: x.sentiment == 'negative', negative_prompt_reply| model | str_parser),
    RunnableLambda(lambda x: "could not find sentiment")
)

chain = classifier_chain | branch_chain

result = chain.invoke({"feedback": "This phone is not worth of its price. OS is too slow"})

print(result)


