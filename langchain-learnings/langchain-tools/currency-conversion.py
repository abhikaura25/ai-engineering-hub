import requests
from langchain_core.tools import tool, StructuredTool, BaseTool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv
from typing import Annotated
from langchain_core.tools import InjectedToolArg

load_dotenv()

@tool
def get_conversion_rate(from_currency: str, to_currency: str) -> float:
    """
    This function fetches the currency conversion factor between a given base currency and a target currency
    """
    url = f'https://v6.exchangerate-api.com/v6/c754eab14ffab33112e380ca/pair/{from_currency}/{to_currency}'

    response = requests.get(url)

    return response.json()

@tool
def convert_currency(amount: float, conversion_rate: Annotated[float, InjectedToolArg]) -> float:
    """
    This function converts a given amount from a base currency to a target currency
    """
    return amount * conversion_rate

llm = ChatOpenAI(temperature=0).bind_tools([get_conversion_rate, convert_currency])

tools = {
    "get_conversion_rate": get_conversion_rate,
    "convert_currency": convert_currency
}

from langchain_core.messages import ToolMessage

messages = [HumanMessage(content="Convert 100 USD to INR")]

ai_message = llm.invoke(messages)
messages.append(ai_message)

# Store the conversion rate to inject into convert_currency
stored_conversion_rate = None

# Process tool calls in a loop until we get a final response
while ai_message.tool_calls:
    for tool_call in ai_message.tool_calls:
        tool_name = tool_call['name']
        tool_args = tool_call['args']

        print(f"Calling tool: {tool_name} with args: {tool_args}")

        # Handle convert_currency specially - inject the stored conversion rate
        if tool_name == "convert_currency":
            tool_args['conversion_rate'] = stored_conversion_rate
            print(f"Injected conversion_rate: {stored_conversion_rate}")

        # Execute the tool
        tool_result = tools[tool_name].invoke(tool_args)

        # If it's the conversion rate, extract and store the rate
        if tool_name == "get_conversion_rate" and isinstance(tool_result, dict):
            stored_conversion_rate = tool_result.get('conversion_rate', 1.0)
            print(f"Stored conversion rate: {stored_conversion_rate}")

        print(f"Tool result: {tool_result}")

        # Add tool message to conversation
        messages.append(ToolMessage(content=str(tool_result), tool_call_id=tool_call['id']))

    # Get next response from LLM
    ai_message = llm.invoke(messages)
    messages.append(ai_message)

# Print final response
print(f"\nFinal answer: {ai_message.content}")