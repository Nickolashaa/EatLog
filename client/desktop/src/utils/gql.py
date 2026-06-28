import httpx

from ..config import API_URL
from ..graphql.client import Client

client = Client(url=f"{API_URL}/graphql")


def health_check() -> bool:
    try:
        return httpx.get(f"{API_URL}/health", timeout=5.0).status_code == 200
    except Exception:
        return False
