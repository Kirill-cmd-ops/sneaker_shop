from email.message import EmailMessage


def get_message(
    sender_gmail: str,
    recipient_gmail: str,
    email_title: str,
    body_title: str,
) -> EmailMessage:
    message = EmailMessage()
    message["From"] =  sender_gmail
    message["To"] = recipient_gmail
    message["Subject"] = email_title
    message.set_content(body_title)

    return message
