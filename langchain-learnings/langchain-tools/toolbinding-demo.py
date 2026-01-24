from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from dotenv import load_dotenv

load_dotenv()

@tool
def multiply_tool(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

@tool
def add_tool(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

llm = ChatOpenAI(temperature=0).bind_tools([multiply_tool, add_tool])

prompt = "Multiply 6 and 7"

messages = [HumanMessage(content=prompt)]
response = llm.invoke(messages)

# Access tool calls from the response
if response.tool_calls:
    for tool_call in response.tool_calls:
        print(f"Tool: {tool_call['name']}, Args: {tool_call['args']}")
        # Execute the tool
        if tool_call['name'] == 'multiply_tool':
            result = multiply_tool.invoke(tool_call['args'])
            messages.append(result)
        elif tool_call['name'] == 'add_tool':
            result = add_tool.invoke(tool_call['args'])
            messages.append(result)

        print(f"Result: {result}")
else:
    print(response.content)