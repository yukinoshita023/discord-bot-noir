# audio_queue.py
import asyncio

class AudioQueue:
    def __init__(self):
        self.queue = asyncio.Queue()
        self.is_playing = False

    async def enqueue(self, voice_client, source):
        await self.queue.put((voice_client, source))
        if not self.is_playing:
            self.is_playing = True
            await self._play_next()

    async def _play_next(self):
        while not self.queue.empty():
            vc, source = await self.queue.get()

            finished = asyncio.Event()

            def after_playing(error):
                if error:
                    print(f"再生中エラー: {error}")
                finished.set()

            vc.play(source, after=after_playing)
            await finished.wait()
            self.queue.task_done()

        self.is_playing = False
