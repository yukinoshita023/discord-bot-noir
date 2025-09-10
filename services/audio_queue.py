import asyncio
from collections import deque

class AudioQueue:
    def __init__(self):
        self._q = deque()
        self._lock = asyncio.Lock()
        self._processing = False

    async def enqueue(self, coro):
        self._q.append(coro)
        if not self._processing:
            await self._drain()

    async def _drain(self):
        self._processing = True
        try:
            while self._q:
                job = self._q.popleft()
                await job
        finally:
            self._processing = False
