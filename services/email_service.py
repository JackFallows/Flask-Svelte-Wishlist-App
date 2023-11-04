import os
import smtplib, ssl
import html
from typing import List
from email.message import EmailMessage

SMTP_EMAIL = os.environ.get("SMTP_EMAIL") # the email address from which emails will be sent
SMTP_SERVER = os.environ.get("SMTP_SERVER") # the URL of the SMTP server
SMTP_PORT = os.environ.get("SMTP_PORT") # the port of the SMTP server
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD") # the password for the email account from which emails will be sent

def is_email_configured():
    return SMTP_EMAIL is not None and SMTP_SERVER is not None and SMTP_PORT is not None and SMTP_PASSWORD is not None

class Email():
    def __init__(self, email: EmailMessage):
        self.email = email
    
    def to(self, receiver_emails: List[str]):
        if not is_email_configured():
            return
        
        self.email["Bcc"] = receiver_emails
        
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(self.email)

def send_share_email(subject: str, message: str):
    email = EmailMessage()
    email['Subject'] = subject
    email["From"] = SMTP_EMAIL
    
    email.set_content(f"""\
    <html>
    <body>
        <p>
        {html.escape(message)}<br />
    Log into the website to see their gift ideas!<br />
    - Wishlist App
        </p>
    </body>
    </html>
    """, subtype='html')
    
    return Email(email)
        
def send_update_email(subject: str, message: str):
    email = EmailMessage()
    email['Subject'] = subject
    email["From"] = SMTP_EMAIL
    
    email.set_content(f"""\
    <html>
    <body>
        <p>
        {html.escape(message)}<br />Log into the website to see what's new.<br />
    - Wishlist App
        </p>
    </body>
    </html>
    """, subtype='html')
    
    return Email(email)

def send_owner_bought_email(subject: str, message: str):
    email = EmailMessage()
    email['Subject'] = subject
    email["From"] = SMTP_EMAIL
    
    email.set_content(f"""\
    <html>
    <body>
        <p>
        {html.escape(message)}<br />
    - Wishlist App
        </p>
    </body>
    </html>
    """, subtype='html')
    
    return Email(email)
