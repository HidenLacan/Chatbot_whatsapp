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

from langchain.llms import OpenAI
from langchain.tools import Tool
from langchain.agents import create_openai_functions_agent
from decouple import config
import wikipedia

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
    """Busca en Wikipedia usando LangChain y devuelve los resultados."""
    
    # Inicializa el modelo de lenguaje de OpenAI
    llm = OpenAI(temperature=0, openai_api_key=config("OPENAI_API_KEY"))
    
    # Define la herramienta para Wikipedia
    tools = [
        Tool.from_function(
            name="wikipedia", 
            func=wikipedia_search_func, 
            description="Busca en Wikipedia una consulta dada y devuelve un resumen."
        )
    ]

    # Crea el agente sin un prompt personalizado
    agent = create_openai_functions_agent(tools=tools, llm=llm)

    # Ejecuta el agente para obtener una respuesta de Wikipedia
    return agent.run(query)
