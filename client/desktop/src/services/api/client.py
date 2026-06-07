import httpx

from ...config import API_URL

client = httpx.Client(base_url=API_URL, timeout=10.0)


def health_check() -> bool:
    try:
        resp = client.get("/health", timeout=5.0)
        return resp.status_code == 200
    except Exception:
        return False
