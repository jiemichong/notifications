from os import environ
import smtplib
import ssl

PORT = 465  # For SSL
PASSWORD = environ.get('password')
SENDER_EMAIL = environ.get('sender_email')
SMTP_EMAIL = environ.get('smtp_email')

# Create a secure SSL context
context = ssl.create_default_context()

server = smtplib.SMTP_SSL(SMTP_EMAIL, PORT, context=context)
try:
    server.login(SENDER_EMAIL, PASSWORD)
except Exception as e:
    print("smtp login failed: ", e)
