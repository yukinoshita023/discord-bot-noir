import discord
import os
from gtts import gTTS
import subprocess
import asyncio

VOICE_TMP_DIR = "voice_tmp"

if not os.path.exists(VOICE_TMP_DIR):
    os.makedirs(VOICE_TMP_DIR)

async def play_tts(bot, vc, text, speed=1.5):
    tts = gTTS(text=text, lang="ja")
    filename = os.path.join(VOICE_TMP_DIR, "vc_announce.mp3")
    tts.save(filename)

    temp_filename = os.path.join(VOICE_TMP_DIR, "vc_announce_temp.mp3")
    subprocess.run([
        'ffmpeg', '-y', '-i', filename, '-filter:a', f'atempo={speed}', temp_filename, '-loglevel', 'quiet',
    ])

    source = discord.FFmpegPCMAudio(temp_filename)

    async def cleanup():
        await asyncio.sleep(1)
        if os.path.exists(filename):
            os.remove(filename)
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

    await bot.audio_queue.enqueue(vc, source)
    asyncio.create_task(cleanup())
