import asyncio

from microservices.auth_service.auth_service.auth.seeds import run_seeds


def start_seeds():
    asyncio.run(run_seeds())


if __name__ == "__main__":
    start_seeds()
