import os
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
import requests
from dotenv import load_dotenv
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.prebuilt import create_react_agent


load_dotenv()

llm = ChatOpenAI()

ACCESS_KEY_WEATHER_API = os.getenv('ACCESS_KEY_WEATHER_API')

@tool
def get_weather_data(city: str) -> str:
    """
    This function fetches the current weather data for a given city
    """
    url = f'https://api.weatherstack.com/current?access_key={ACCESS_KEY_WEATHER_API}&query={city}'

    response = requests.get(url)

    return response.json()


search_tool = DuckDuckGoSearchRun()

# Create agent using langgraph
agent = create_react_agent(llm, tools=[search_tool, get_weather_data])

# Invoke the agent
response = agent.invoke({"messages": [("user", "Find the capital of Punjab, then find it's current weather condition")]})

print(response["messages"][-1].content)




