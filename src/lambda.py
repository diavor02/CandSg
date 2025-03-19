import re
import json
import pandas as pd
import smtplib
import ssl
from email.message import EmailMessage
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


EMAILS= ["darius.iavorschi@gmail.com", "robertcosta378@gmail.com", "burkettj2486@gmail.com"]

URI = "mongodb+srv://dariusiavorschi:rge3zdZplVgaDM5j@cluster0.i5iph.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

CLIENT = MongoClient(URI, server_api=ServerApi('1'))

try:
    CLIENT.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


def extract_key(key_val, body_content):
    pattern = fr"{key_val}:(.*?),"

    match = re.search(pattern, body_content)

    if match:
        key = match.group(1)
    else:
        key = "Not found"

    return key

def input_doc_to_MongoDB(document):

    print(document)

    db = CLIENT['db1'] 
    collection = db['cl1']  

    result = collection.insert_one(document)

    print(f"Document inserted with ID: {result.inserted_id}")

def parse_event(input_string):
    pattern = r"'body': '{(.*?)}'"

    print("input_string: ", input_string)
    
    match = re.search(pattern, input_string)
    
    try:

        body_content = match.group(1)

        print("body_content: ", body_content)

        body_content += ','

        signal = extract_key("Signal", body_content)
        time = extract_key("Time", body_content)
        ticker = extract_key("Ticker", body_content)
        price = extract_key("Price", body_content)

        print("signal: ", signal)
        print("time: ", time)
        print("ticker: ", ticker)
        print("price: ", price)

        document = {"Signal": signal, 
                "Time": time,
                "Ticker": ticker,
                "Price": price}

        print("final document as string: ", str(document))
        
        input_doc_to_MongoDB(document)

        return document

    except Exception as e:
        print(f"Error: {e}")


def send_email(event, email: str) -> None:
    email_sender = 'sendstockupdate@gmail.com'
    email_password = 'bdvj oexx rgeg epkf'
    email_receiver = email

    subject = 'Update'
    body = str(event)

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

    print("Email sent successfully")


def lambda_handler(event, context) -> dict:

    try:
        for email in EMAILS:
            send_email(str(json.dumps(event)), email)
            # send_email(str(parse_event(str(event))), email)

        return {"statusCode": 200, "body": "Notification sent."}

    except Exception as error:
        print(f"Critical error in lambda_handler: {str(error)}")
        return {"statusCode": 500, "body": f"Server Error: {str(error)}"}
    
    