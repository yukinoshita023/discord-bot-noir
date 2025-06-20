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
        'ffmpeg', '-i', filename, '-filter:a', f'atempo={speed}', temp_filename, '-loglevel', 'quiet',
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

def setup(bot):
    @bot.event
    async def on_voice_state_update(member, before, after):
        if before.channel != after.channel:
            display_name = member.display_name

            vc = None
            if after.channel and bot.user in after.channel.members:
                vc = discord.utils.get(bot.voice_clients, guild=member.guild)
                if vc and vc.is_connected():
                    await play_tts(bot, vc, f"{display_name} さんが参加しました", speed=2.0)

            elif before.channel and bot.user in before.channel.members:
                vc = discord.utils.get(bot.voice_clients, guild=member.guild)
                if vc and vc.is_connected():
                    await play_tts(bot, vc, f"{display_name} さんが退出しました", speed=2.0)
