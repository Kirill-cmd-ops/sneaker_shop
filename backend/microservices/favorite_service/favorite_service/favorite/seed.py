import asyncio

from microservices.favorite_service.favorite_service.favorite.seeds import run_seeds


def start_seeds():
    asyncio.run(run_seeds())


if __name__ == "__main__":
    start_seeds()
