from celery_client.celery_connection.celery_getter import get_celery
from message_sender.send_message import send_message

celery_client = get_celery("service", broker="redis://:Meteor906587@redis_queue:6379/0")


@celery_client.task(name="cart.view")
def handle_cart_view(
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
