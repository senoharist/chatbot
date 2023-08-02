import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sqlite3

# Email configuration
nama = 'chel'
sender_email = 'scyllainsight@pratesis.com'
receiver_email = 'suseno_haris@pratesis.com'
subject = 'coba kirim email dari sender pratomo'
message = f"dear {nama} -- \nini dari chatbot. \ntolong diabaikan saja --18072023."

# Create a multipart message
email_message = MIMEMultipart()
email_message['From'] = sender_email
email_message['To'] = receiver_email
email_message['Subject'] = subject

# Attach the message to the email
email_message.attach(MIMEText(message, 'plain'))

# SMTP server configuration
smtp_server = 'mail.pratesis.com'
smtp_port = 587
smtp_username = 'scyllainsight@pratesis.com'
smtp_password = 'Pratesis123!'

try:
    # Create a secure SSL/TLS connection to the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()

        # Log in to the SMTP server
        server.login(smtp_username, smtp_password)

        # Send the email
        server.send_message(email_message)

    print('Email sent successfully!')
except Exception as e:
    print('An error occurred while sending the email:', str(e))
