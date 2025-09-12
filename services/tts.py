import discord
import asyncio
import tempfile
import os
import edge_tts
from services.audio_queue import AudioQueue
from config import VOICE_MODEL

def speed_to_rate(speed: float) -> str:
    pct = int((speed - 1.0) * 100)
    sign = "+" if pct >= 0 else ""
    return f"{sign}{pct}%"

async def synthesize(text: str, speed: float = 2.0, voice: str = VOICE_MODEL) -> str:
    rate = speed_to_rate(speed)

    fd, path = tempfile.mkstemp(prefix="tts_", suffix=".mp3")
    os.close(fd)

    communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate)
    await communicate.save(path)
    return path

async def play_file(vc: discord.VoiceClient, path: str):
    def after_play(err):
        if err:
            print("play error:", err)

    audio = discord.FFmpegPCMAudio(path)
    vc.play(audio, after=after_play)

    try:
        while vc.is_playing() or vc.is_paused():
            await asyncio.sleep(0.1)
    finally:
        try:
            os.remove(path)
        except OSError:
            pass

async def play_tts(bot, vc: discord.VoiceClient, text: str, speed: float = 2.0):
    async def job():
        path = await synthesize(text, speed)
        await play_file(vc, path)

    await bot.audio_queue.enqueue(job())

async def play_wav(bot, vc: discord.VoiceClient, path: str):
    async def job():
        def after_play(err):
            if err:
                print("play error:", err)

        audio = discord.FFmpegPCMAudio(path)
        vc.play(audio, after=after_play)

        while vc.is_playing() or vc.is_paused():
            await asyncio.sleep(0.1)

    await bot.audio_queue.enqueue(job())
