# # Standard library import
# import logging
# import os

# # Third-party imports
# from twilio.rest import Client
# from decouple import config


# from langchain.llms import OpenAI
# from langchain.agents import initialize_agent, AgentType
# from langchain.tools import Tool
# from decouple import config
# import wikipedia




# # Twilio setup
# account_sid = config("TWILIO_ACCOUNT_SID")
# auth_token = config("TWILIO_AUTH_TOKEN")
# client = Client(account_sid, auth_token)
# twilio_number = config('TWILIO_NUMBER')

# # Set up logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Sending message logic through Twilio Messaging API
# def send_message(to_number, body_text):
#     try:
#         message = client.messages.create(
#             from_=f"whatsapp:{twilio_number}",
#             body=body_text,
#             to=f"whatsapp:{to_number}"
#         )
#         logger.info(f"Message sent to {to_number}: {message.body}")
#     except Exception as e:
#         logger.error(f"Error sending message to {to_number}: {e}")
        

# def wikipedia_search_func(query):
#     try:
#         summary = wikipedia.summary(query, sentences=2)
#         return summary
#     except wikipedia.exceptions.DisambiguationError as e:
#         return f"Tu consulta es ambigua. Opciones posibles: {e.options}"
#     except wikipedia.exceptions.PageError:
#         return "No se encontró una página que coincida con tu consulta."
#     except Exception as e:
#         return f"Ocurrió un error: {str(e)}"

# def search_wikipedia(query):
#     llm = OpenAI(temperature=0, openai_api_key=config("OPENAI_API_KEY"))
#     tools = [
#         Tool(
#             name="wikipedia", 
#             func=wikipedia_search_func, 
#             description="Busca en Wikipedia y devuelve un resumen."
#         )
#     ]
#     agent = initialize_agent(
#         tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True
#     )
#     return agent.run(query)



# Standard library imports
import logging

# Third-party imports
from twilio.rest import Client
from decouple import config
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
import wikipedia

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

def wikipedia_search_func(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Tu consulta es ambigua. Opciones posibles: {e.options}"
    except wikipedia.exceptions.PageError:
        return "No se encontró una página que coincida con tu consulta."
    except Exception as e:
        return f"Ocurrió un error: {str(e)}"

def search_wikipedia(query):
    llm = ChatOpenAI(temperature=0, openai_api_key=config("OPENAI_API_KEY"))
    tools = [
        Tool(
            name="wikipedia",
            func=wikipedia_search_func,
            description="Busca en Wikipedia y devuelve un resumen."
        )
    ]
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True
    )
    return agent.run(query)
