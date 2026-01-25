import asyncio

from favorite_service.favorite.seeds import run_seeds

def start_seeds():
    asyncio.run(run_seeds())