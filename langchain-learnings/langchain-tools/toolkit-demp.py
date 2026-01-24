from langchain_core.tools import tool, StructuredTool, BaseTool

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

@tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

class MathToolKit:
    """A toolkit for math operations."""

    def get_tools(self):
        return [multiply, add]

toolkit = MathToolKit()
tools = toolkit.get_tools()
for t in tools:
    result = t.invoke({'a': 5, 'b': 3})
    print(f"Result of {t.name}: {result}")

