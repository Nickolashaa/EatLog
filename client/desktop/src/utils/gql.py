from typing import Any, cast

import httpx
from gql.client import Client

from ..config import API_URL


class _ClientProxy:
    def __getattr__(self, name: str) -> Any:
        async def call(*args: Any, **kwargs: Any) -> Any:
            async with Client(url=f"{API_URL}/graphql") as client_:
                return await getattr(client_, name)(*args, **kwargs)

        return call


client = cast(Client, _ClientProxy())


def health_check() -> bool:
    try:
        return httpx.get(f"{API_URL}/health", timeout=5.0).status_code == 200
    except Exception:
        return False
