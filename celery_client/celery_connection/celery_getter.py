from celery import Celery


def get_celery(
        name_service: str,
        broker: str = "redis://:Meteor906587@redis_queue:6379/0",
):
    return Celery(
            main=name_service,
            broker=broker,
        )
