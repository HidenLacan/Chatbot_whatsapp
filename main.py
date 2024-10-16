
# from fastapi import FastAPI, Form, Depends, Request
# from decouple import config

# #change database
# from sqlalchemy.exc import SQLAlchemyError
# from sqlalchemy.orm import Session
# #########

# # Internal imports
# from model import Conversation, SessionLocal
# from utils import send_message, logger, search_wikipedia



# #### current time and day
# from datetime import datetime
# today = datetime.today()
# formatted_date = today.strftime("%D %m %y")

# #### airtable integration
# from pyairtable import Table
# from decouple import config

# # Airtable configuration to env
# air_token = config("AIRTABLE_TOKEN")
# base_id = config("BASE_ID")  # Your base ID
# table_name = config("TABLE_NAME")  # Your table name


# app = FastAPI()
# @app.get("/")
# def read_root():
#     return {"Hello": "World 2"}



# # Connect to the Airtable table
# table = Table(air_token, base_id, table_name)

# # Function to add a record
# def save_ticket(ticket_number, description, start_date, phone_number):
#     data = {
#         "Ticket_Number": ticket_number,
#         "Description": description,
#         "Start date": start_date,
#         "Phone_Number": phone_number
#     }
#     table.create(data)



# # Dependency
# #def get_db():
# #    try:
# #        db = SessionLocal()
# #        yield db
# #   finally:
# #        db.close()

# @app.post("/message")
# async def reply(request: Request, Body: str = Form()):
#     # Extract the phone number from the incoming webhook request
#     form_data = await request.form()
#     whatsapp_number = form_data['From'].split("whatsapp:")[-1]
#     print(f"Sending the LangChain response to this number: {whatsapp_number}")
    
#     #save_ticket(whatsapp_number, Body, formatted_date, whatsapp_number)

#     # Get the generated text from the LangChain agent
#     langchain_response = search_wikipedia(Body)
    

#     # Store the conversation in the airtable
#     try:
#         save_ticket(whatsapp_number, Body, formatted_date, whatsapp_number)
#         logger.info(f"Conversation stored for WhatsApp number: {whatsapp_number}")
#     except Exception as e:
#         logger.error(f"Error storing conversation in Airtable: {e}")
#     send_message(whatsapp_number, langchain_response)
#     return ""


from fastapi import FastAPI, Form, Request
from decouple import config
from datetime import datetime
import logging

# Importaciones de terceros
from pyairtable import Table

# Importaciones internas
from utils import send_message, logger, search_wikipedia

app = FastAPI()

# Configuración de Airtable
air_token = config("AIRTABLE_TOKEN")
base_id = config("BASE_ID")  # Tu ID de base
table_name = config("TABLE_NAME")  # Tu nombre de tabla

# Conexión a la tabla de Airtable
table = Table(air_token, base_id, table_name)

# Función para agregar un registro a Airtable
def save_ticket(ticket_number, description, start_date, phone_number):
    data = {
        "Ticket_Number": ticket_number,
        "Description": description,
        "Start date": start_date,
        "Phone_Number": phone_number
    }
    try:
        table.create(data)
        logger.info(f"Registro creado en Airtable para el número: {phone_number}")
    except Exception as e:
        logger.error(f"Error al crear el registro en Airtable: {e}")

@app.get("/")
def read_root():
    return {"Hello": "World 2"}

@app.post("/message")
async def reply(request: Request, Body: str = Form()):
    # Extraer el número de WhatsApp del webhook entrante
    form_data = await request.form()
    whatsapp_number = form_data['From'].split("whatsapp:")[-1]
    print(f"Enviando respuesta de LangChain a este número: {whatsapp_number}")

    # Obtener la respuesta generada por LangChain
    langchain_response = search_wikipedia(Body)

    # Obtener la fecha y hora actuales
    today = datetime.now()
    formatted_date = today.strftime("%Y-%m-%d %H:%M:%S")

    # Almacenar la conversación en Airtable
    save_ticket(
        ticket_number=whatsapp_number,
        description=Body,
        start_date=formatted_date,
        phone_number=whatsapp_number
    )

    # Enviar respuesta al usuario vía WhatsApp
    send_message(whatsapp_number, langchain_response)
    return ""
