import smtplib
from email.mime.text import MIMEText
import os

def send_email(subject, body):
    sender = os.getenv("EMAIL_FROM")
    password = os.getenv("EMAIL_PASSWORD")
    receiver = os.getenv("EMAIL_TO")

    if not receiver:
        raise ValueError("TO_EMAIL is not set in .env file")

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())
