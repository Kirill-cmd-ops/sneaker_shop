import asyncio

from cart_service.cart.seeds import run_seeds

def start_seeds():
    asyncio.run(run_seeds())