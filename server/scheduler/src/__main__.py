import asyncio
import logging

from .scheduler import build_scheduler


async def main() -> None:
    logging.basicConfig(level=logging.INFO)

    build_scheduler().start()

    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
