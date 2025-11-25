import smtplib

from message_sender.create_message import get_message


def send_message(
    hostname: str,
    port: int,
    start_tls: bool,
    username: str,
    password: str,
    sender_gmail: str,
    recipient_gmail: str,
    email_title: str,
    body_title: str,
):
    message = get_message(
        sender_gmail=sender_gmail,
        recipient_gmail=recipient_gmail,
        email_title=email_title,
        body_title=body_title,
    )

    with smtplib.SMTP(hostname, port) as smtp:
        if start_tls:
            smtp.starttls()

        smtp.login(username, password)
        smtp.send_message(message)
