import os
from decouple import config
from langchain.tools import Tool
from langchain.agents import create_openai_functions_agent
from langchain_openai import OpenAI

# Initialize the OpenAI LLM with the updated import
llm = OpenAI(temperature=0, openai_api_key=config("OPENAI_API_KEY"))

# Load tools (e.g., Wikipedia)
tools = [Tool.from_function("wikipedia", llm=llm)]  # Update tool loading as per new LangChain version

# Create agent using the updated function
agent = create_openai_functions_agent(tools=tools, llm=llm)


# Example usage of the agent
response = agent.invoke({"input": "What is the capital of France?"})
print(response)
