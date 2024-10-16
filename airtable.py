#### airtable integration
from pyairtable import Table
from decouple import config

# Airtable configuration to env
AIRTABLE_TOKEN = config("AIRTABLE_TOKEN")
BASE_ID = config("BASE_ID")  # Your base ID
TABLE_NAME = config("TABLE_NAME")  # Your table name

# Connect to the Airtable table
table = Table(AIRTABLE_TOKEN, BASE_ID, TABLE_NAME)



def save_ticket(ticket_number, description, start_date, phone_number):
    data = {
        "Ticket_Number": ticket_number,
        "Description": description,
        "Start date": start_date,
        "Phone_Number": phone_number
    }
    table.create(data)