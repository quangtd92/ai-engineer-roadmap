# Unit tests for StatusClient (Day 16)
import httpx
import pytest
from ai_assistant_platform.core.errors import ExternalServiceError
from ai_assistant_platform.services.status_client import StatusClient


def handler(request: httpx.Request) -> httpx.Response:
    # Trả về response giả lập
    return httpx.Response(200, json={"status": "ok"})


@pytest.mark.anyio
async def test_get_status_success():
    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as client:
        status_client = StatusClient(client)
        result = await status_client.get_status("https://httpbin.org/get")
        assert result == {"status": "ok"}


def handler_timeout(request: httpx.Request) -> httpx.Response:
    # Trả về response giả lập
    raise httpx.TimeoutException("Time out")


@pytest.mark.anyio
async def test_get_status_timeout():
    transport = httpx.MockTransport(handler_timeout)
    async with httpx.AsyncClient(transport=transport) as client:
        status_client = StatusClient(client, timeout=1)
        with pytest.raises(ExternalServiceError):
            await status_client.get_status("https://httpbin.org/get")


def handler_http_500(request: httpx.Request) -> httpx.Response:
    return httpx.Response(500, json={"error": "server error"})


@pytest.mark.anyio
async def test_get_status_http_500():
    transport = httpx.MockTransport(handler_http_500)
    async with httpx.AsyncClient(transport=transport) as client:
        status_client = StatusClient(client, timeout=1)
        with pytest.raises(ExternalServiceError):
            await status_client.get_status("https://httpbin.org/get")


def handler_request_error(request: httpx.Request) -> httpx.Response:
    raise httpx.ConnectError("Connection refused")


@pytest.mark.anyio
async def test_get_status_request_error():
    transport = httpx.MockTransport(handler_request_error)
    async with httpx.AsyncClient(transport=transport) as client:
        status_client = StatusClient(client, timeout=1)
        with pytest.raises(ExternalServiceError):
            await status_client.get_status("https://httpbin.org/get")