import asyncio

from sneaker_details_service.sneaker_details.seeds import run_seeds

def start_seeds():
    asyncio.run(run_seeds())