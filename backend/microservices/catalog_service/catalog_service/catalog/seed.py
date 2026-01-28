import asyncio

from microservices.catalog_service.catalog_service.catalog.seeds import run_seeds


def start_seeds():
    asyncio.run(run_seeds())


if __name__ == "__main__":
    start_seeds()
