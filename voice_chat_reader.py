import discord
import asyncio
import os
import re
from gtts import gTTS

class VoiceChatReader:
    def __init__(self, bot, speed=1.5):
        self.bot = bot
        self.speed = speed
        self.voice_tmp_dir = os.path.join(os.path.dirname(__file__), "voice_tmp")

    async def on_message(self, message):
        if message.author.bot:
            return

        if any(attachment.content_type and attachment.content_type.startswith(("image/", "video/")) for attachment in message.attachments):
            return

        vc = discord.utils.get(self.bot.voice_clients, guild=message.guild)
        if vc and vc.is_connected():
            member = message.guild.get_member(message.author.id)
            if member and member.voice:
                if member.voice.channel == vc.channel:
                    if member.voice.self_mute or member.voice.mute:
                        text = self.filter_message(message.content)
                        if text:
                            await self.read_text_in_vc(vc, text)

    def filter_message(self, text):
        emoji_pattern = re.compile(r'<:.+?:\d+>|<a:.+?:\d+>|[\U00010000-\U0010ffff]')
        url_pattern = re.compile(r'https?://\S+|www\.\S+')

        text = emoji_pattern.sub('', text)
        if url_pattern.search(text):
            text = "URL省略"

        return text.strip()

    async def read_text_in_vc(self, vc, text):
        tts = gTTS(text=text, lang="ja")
        filename = os.path.join(self.voice_tmp_dir, "speech.mp3")
        tts.save(filename)

        ffmpeg_options = f'-filter:a "atempo={self.speed}"'

        vc.play(discord.FFmpegPCMAudio(filename, options=ffmpeg_options), after=lambda e: os.remove(filename))
        while vc.is_playing():
            await asyncio.sleep(1)
