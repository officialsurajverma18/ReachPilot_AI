import smtplib
from email.message import EmailMessage
from flask import current_app


def send_email(to, subject, message):
    config = current_app.config
    if not all((config.get("SMTP_HOST"), config.get("SMTP_USERNAME"), config.get("SMTP_PASSWORD"), config.get("SMTP_FROM"))):
        raise RuntimeError("Email is not configured. Add SMTP settings to server environment variables.")
    email = EmailMessage()
    email["From"], email["To"], email["Subject"] = config["SMTP_FROM"], to, subject
    email.set_content(message)
    with smtplib.SMTP(config["SMTP_HOST"], config["SMTP_PORT"], timeout=20) as server:
        server.starttls()
        server.login(config["SMTP_USERNAME"], config["SMTP_PASSWORD"])
        server.send_message(email)
