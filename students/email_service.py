
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings


def send_registration_email(to_email, student_id, name):
    sender_email = settings.EMAIL_HOST_USER
    sender_password = settings.EMAIL_HOST_PASSWORD

    subject = "Student Registration Successful"
    body = f"""
Hello {name},

Your registration was successful.

Your Registration ID is: {student_id}

Thank you.
"""

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    server.starttls()
    server.login(sender_email, sender_password)
    server.send_message(msg)
    server.quit()
