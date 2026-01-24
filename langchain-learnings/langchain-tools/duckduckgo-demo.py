from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools import ShellTool
from langchain_core.tools import tool, StructuredTool, BaseTool
from pydantic import BaseModel, Field
from typing import Type

#### Duck Duck Go Search Run ######

search_tool = DuckDuckGoSearchRun()

results = search_tool.invoke('Bangladesh cricket news')

print(results)

### Shell command tool run ####

shell_tool = ShellTool()

shell_result = shell_tool.invoke('whoami')
print(shell_result)

def multiply_func(a:int,b:int) -> int:
    """Multiply two numbers"""
    return a*b

@tool
def multiply_tool(a:int, b:int) -> int:
    """Multiply two numbers"""
    return a*b

result = multiply_tool.invoke({'a': 2, 'b': 3})
print(result)

class MultiplyInput(BaseModel):
    a: int = Field(description="the first number to multiply")
    b: int = Field(description="second number to multiply")

multiply_tool = StructuredTool.from_function(
    func=multiply_func,
    name="multiply",
    description="Multiply two numbers",
    args_schema=MultiplyInput
)

final_result = multiply_tool.invoke({'a': 2, 'b': 3})

print(final_result)


############################################################
class MultiplyTool(BaseTool):
    name: str = "multiply"
    description: str = "Multiply two numbers"
    args_schema: Type[BaseModel] = MultiplyInput

    def _run(self, a: int, b: int) -> int:
        return a * b


final_tool = MultiplyTool()

final_result_1 = final_tool.invoke({'a': 4, 'b': 3})
print(final_result_1)
