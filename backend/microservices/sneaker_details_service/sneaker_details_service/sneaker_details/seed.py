import asyncio

from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.seeds import run_seeds


def start_seeds():
    asyncio.run(run_seeds())


if __name__ == "__main__":
    start_seeds()
