import asyncio

from stock_notification_service.stock_notification.seeds import run_seeds

def start_seeds():
    asyncio.run(run_seeds())