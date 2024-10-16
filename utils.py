# Standard library import
import logging
import os

# Third-party imports
from twilio.rest import Client
from decouple import config
from langchain.tools import Tool
from langchain_openai import OpenAI
from langchain.agents import create_openai_functions_agent

# Twilio setup
account_sid = config("TWILIO_ACCOUNT_SID")
auth_token = config("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)
twilio_number = config('TWILIO_NUMBER')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sending message logic through Twilio Messaging API
def send_message(to_number, body_text):
    try:
        message = client.messages.create(
            from_=f"whatsapp:{twilio_number}",
            body=body_text,
            to=f"whatsapp:{to_number}"
        )
        logger.info(f"Message sent to {to_number}: {message.body}")
    except Exception as e:
        logger.error(f"Error sending message to {to_number}: {e}")

# Wikipedia search logic using updated LangChain
def search_wikipedia(query):
    """Search Wikipedia using LangChain OpenAI wrapper and return results"""
    
    # Initialize the OpenAI LLM
    llm = OpenAI(temperature=0, openai_api_key=config("OPENAI_API_KEY"))
    
    # Load tools for Wikipedia (updated tool API)
    tools = [Tool.from_function(name="wikipedia", func=search_wikipedia, description="Searches Wikipedia")]

    # Define the prompt to guide the agent
    prompt = f"Use the Wikipedia tool to answer the following query: {query}"
    
    # Create the agent with the required prompt
    agent = create_openai_functions_agent(tools=tools, llm=llm, prompt=prompt)
    
    # Run the agent to get a response from Wikipedia
    return agent.invoke({"input": query})
