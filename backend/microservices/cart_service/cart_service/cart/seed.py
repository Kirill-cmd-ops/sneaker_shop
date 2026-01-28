import asyncio

from microservices.cart_service.cart_service.cart.seeds import run_seeds


def start_seeds():
    asyncio.run(run_seeds())


if __name__ == "__main__":
    start_seeds()
