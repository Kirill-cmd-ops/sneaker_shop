import asyncio

from microservices.stock_notification_service.stock_notification_service.stock_notification.seeds import run_seeds


def start_seeds():
    asyncio.run(run_seeds())


if __name__ == "__main__":
    start_seeds()
