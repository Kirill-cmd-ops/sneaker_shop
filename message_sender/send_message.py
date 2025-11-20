import smtplib

from message_sender.create_message import get_message


def send_message(
    hostname: str,
    port: int,
    start_tls: bool,
    username: str,
    password: str,
):
    message = get_message(
        sender_gmail="Sneaker Shop <bondarenkokirill150208@gmail.com>",
        recipient_gmail="kugoshoping@gmail.com",
        email_title="Проверочный код",
        body_title="Ваш проверочный код: 666777",
    )

    with smtplib.SMTP(hostname, port) as smtp:
        if start_tls:
            smtp.starttls()

        smtp.login(username, password)
        smtp.send_message(message)
