import pandas as pd
import smtplib
import ssl
from email.message import EmailMessage

EMAILS= ["darius.iavorschi@gmail.com", "robertcosta378@gmail.com"]

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
            send_email(event, email)

        return {"statusCode": 200, "body": "Notification sent."}

    except Exception as error:
        print(f"Critical error in lambda_handler: {str(error)}")
        return {"statusCode": 500, "body": f"Server Error: {str(error)}"}
    
    