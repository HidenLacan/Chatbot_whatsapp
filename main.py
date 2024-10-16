
from fastapi import FastAPI, Form, Depends, Request
from decouple import config

#change database
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
#########

# Internal imports
from model import Conversation, SessionLocal
from utils import send_message, logger, search_wikipedia



#### current time and day
from datetime import datetime
today = datetime.today()
formatted_date = today.strftime("%D %m %y")

#### airtable integration
from pyairtable import Table
from decouple import config

# Airtable configuration to env
AIRTABLE_TOKEN = config("AIRTABLE_TOKEN")
BASE_ID = config("BASE_ID")  # Your base ID
TABLE_NAME = config("TABLE_NAME")  # Your table name

# Connect to the Airtable table
table = Table(AIRTABLE_TOKEN, BASE_ID, TABLE_NAME)

# Function to add a record
def save_ticket(ticket_number, description, start_date, phone_number):
    data = {
        "Ticket_Number": ticket_number,
        "Description": description,
        "Start date": start_date,
        "Phone_Number": phone_number
    }
    table.create(data)

app = FastAPI()
@app.get("/")
def read_root():
    return {"Hello": "World 2"}

# Dependency
#def get_db():
#    try:
#        db = SessionLocal()
#        yield db
#   finally:
#        db.close()

@app.post("/message")
async def reply(request: Request, Body: str = Form()):
    # Extract the phone number from the incoming webhook request
    form_data = await request.form()
    whatsapp_number = form_data['From'].split("whatsapp:")[-1]
    print(f"Sending the LangChain response to this number: {whatsapp_number}")

    # Get the generated text from the LangChain agent
    langchain_response = search_wikipedia(Body)

    # Store the conversation in the airtable
    try:
        save_ticket(whatsapp_number, Body, formatted_date, whatsapp_number)
        #db.add(conversation)
        #db.commit()
        logger.info(f"Conversation #{save_ticket} stored in database")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error storing conversation in database: {e}")
    send_message(whatsapp_number, langchain_response)
    return ""

