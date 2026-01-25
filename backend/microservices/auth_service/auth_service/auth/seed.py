import asyncio

from auth_service.auth.seeds import run_seeds

def start_seeds():
    asyncio.run(run_seeds())