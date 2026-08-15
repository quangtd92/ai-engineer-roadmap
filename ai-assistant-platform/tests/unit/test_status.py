"""Unit tests for the async status route handler."""

import pytest

from ai_assistant_platform.api.routes.status import get_status


@pytest.mark.anyio
async def test_get_status_handler():
    """Unit test: gọi trực tiếp async handler get_status."""
    response = await get_status()
    assert response == {"status": "ready"}

