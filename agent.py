import os
from decouple import config
from langchain.tools import load_tools
from langchain.agents import create_openai_functions_agent
from langchain_openai import OpenAI

# Initialize LLM
llm = OpenAI(temperature=0, openai_api_key=config("OPENAI_API_KEY"))

# Load Wikipedia tool
tools = load_tools(["wikipedia"], llm=llm)

# Create agent
agent = create_openai_functions_agent(tools=tools, llm=llm, verbose=True)
