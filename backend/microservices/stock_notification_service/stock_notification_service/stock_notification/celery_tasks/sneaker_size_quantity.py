from celery_client.celery_connection.celery_getter import get_celery
from message_sender.send_message import send_message

celery_client = get_celery(
    name_service="sneaker_details_service",
    broker="redis://:Meteor906587@redis_queue:6379/1",
)


@celery_client.task(name="update.quantity")
def process_sneaker_size_quantity_update(
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
