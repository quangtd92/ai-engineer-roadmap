"""Async status endpoint.

Route dùng async def vì status check là I/O-bound operation.
Async cho phép event loop phục vụ request khác trong khi chờ I/O,
khác với CPU-bound work (ví dụ PyTorch inference) không hưởng lợi từ async.
"""

import asyncio

from fastapi import APIRouter

router = APIRouter(
    prefix='/api/v1',
    tags=['status']
)


@router.get("/status")
async def get_status():
    # Minh họa yield: nhường event loop rồi quay lại ngay, không gây delay.
    await asyncio.sleep(0)
    return {"status": "ready"}