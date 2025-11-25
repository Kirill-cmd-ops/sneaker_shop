from celery_client.celery_connection.celery_getter import get_celery
from message_sender.send_message import send_message

celery_client = get_celery("service", broker="redis://:Meteor906587@redis_queue:6379/0")


@celery_client.task(name="request.verify")
def handle_request_verify(
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
    send_message(
        hostname=hostname,
        port=port,
        start_tls=start_tls,
        username=username,
        password=password,
        sender_gmail=sender_gmail,
        recipient_gmail=recipient_gmail,
        email_title=email_title,
        body_title=body_title,
    )


@celery_client.task(name="request.reset")
def handle_request_reset(
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
    send_message(
        hostname=hostname,
        port=port,
        start_tls=start_tls,
        username=username,
        password=password,
        sender_gmail=sender_gmail,
        recipient_gmail=recipient_gmail,
        email_title=email_title,
        body_title=body_title,
    )


@celery_client.task(name="after.verify")
def handle_after_verify(
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
    send_message(
        hostname=hostname,
        port=port,
        start_tls=start_tls,
        username=username,
        password=password,
        sender_gmail=sender_gmail,
        recipient_gmail=recipient_gmail,
        email_title=email_title,
        body_title=body_title,
    )


@celery_client.task(name="after.register")
def handle_after_register(
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
    send_message(
        hostname=hostname,
        port=port,
        start_tls=start_tls,
        username=username,
        password=password,
        sender_gmail=sender_gmail,
        recipient_gmail=recipient_gmail,
        email_title=email_title,
        body_title=body_title,
    )


@celery_client.task(name="after.reset")
def handle_after_reset(
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
    send_message(
        hostname=hostname,
        port=port,
        start_tls=start_tls,
        username=username,
        password=password,
        sender_gmail=sender_gmail,
        recipient_gmail=recipient_gmail,
        email_title=email_title,
        body_title=body_title,
    )
