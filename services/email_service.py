import os
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_EMAIL = os.environ.get("SMTP_EMAIL") # the email address from which emails will be sent
SMTP_SERVER = os.environ.get("SMTP_SERVER") # the URL of the SMTP server
SMTP_PORT = os.environ.get("SMTP_PORT") # the port of the SMTP server
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD") # the password for the email account from which emails will be sent

def send_share_email(receiver_email: str, sender_name: str, sender_email: str, sender_wishlist: str):
    if SMTP_EMAIL is None or SMTP_SERVER is None or SMTP_PORT is None or SMTP_PASSWORD is None:
        return
    
    message = MIMEMultipart("alternative")
    message["Subject"] = f"{sender_name} shared a wishlist with you!"
    message["From"] = SMTP_EMAIL
    message["To"] = receiver_email

    text = f"""\
    {sender_name} ({sender_email}) just shared the wishlist '{sender_wishlist}' with you.
    Log into the website to see their gift ideas!
    - Wishlist App"""
    html = f"""\
    <html>
    <body>
        <p>
        {sender_name} ({sender_email}) just shared the wishlist '{sender_wishlist}' with you.<br />
    Log into the website to see their gift ideas!<br />
    - Wishlist App
        </p>
    </body>
    </html>
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.sendmail(SMTP_EMAIL, receiver_email, message.as_string())
