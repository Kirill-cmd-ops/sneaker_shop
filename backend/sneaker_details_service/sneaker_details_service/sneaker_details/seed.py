import asyncio

from sneaker_details_service.sneaker_details.seeds import run_seeds

if __name__ == "__main__":
    asyncio.run(run_seeds())