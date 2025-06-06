import asyncio

from backend.catalog_service.catalog_service.catalog.seeds import run_seeds

if __name__ == "__main__":
    asyncio.run(run_seeds())