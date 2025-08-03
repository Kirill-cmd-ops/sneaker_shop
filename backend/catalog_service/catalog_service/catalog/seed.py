import asyncio

from catalog_service.catalog.seeds import run_seeds

def start_seeds():
    asyncio.run(run_seeds())