import httpx

from ai_assistant_platform.core.errors import ExternalServiceError


class StatusClient:
    def __init__(
        self, client: httpx.AsyncClient | None = None, timeout: float = 2
    ) -> None:
        self.client = client
        self.timeout = timeout

    async def get_status(self, url: str) -> dict:
        try:
            response = await self.client.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException as exc:
            raise ExternalServiceError("Request timeout") from exc
        except httpx.HTTPStatusError as exc:
            raise ExternalServiceError("Bad response") from exc
        except httpx.RequestError as exc:
            raise ExternalServiceError("Request error") from exc
