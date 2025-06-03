import discord
import asyncio
import os
import re
from audio_queue import TTSPlayer

class VoiceChatReader:
    def __init__(self, bot, tts_player: TTSPlayer, speed=1.5):
        self.bot = bot
        self.tts_player = tts_player
        self.speed = speed

    async def on_message(self, message):
        if message.author.bot:
            return

        if any(attachment.content_type and attachment.content_type.startswith(("image/", "video/")) for attachment in message.attachments):
            return

        vc = discord.utils.get(self.bot.voice_clients, guild=message.guild)
        if not vc or not vc.is_connected():
            return

        member = message.guild.get_member(message.author.id)
        if not member or not member.voice or member.voice.channel != vc.channel:
            return

        if not (member.voice.self_mute or member.voice.mute):
            return

        if not self.is_same_category(member.voice.channel, message.channel):
            return

        text = self.filter_message(message.content)
        if text:
            await self.tts_player.enqueue_tts(f"{member.display_name} さん、{text}", speed=self.speed)

    def is_same_category(self, voice_channel, text_channel):
        return (voice_channel.category and text_channel.category and voice_channel.category.id == text_channel.category.id)

    def filter_message(self, text):
        emoji_pattern = re.compile(r'<:.+?:\d+>|<a:.+?:\d+>|[\U00010000-\U0010ffff]')
        url_pattern = re.compile(r'https?://\S+|www\.\S+')

        text = emoji_pattern.sub('', text)
        if url_pattern.search(text):
            text = "URL省略"

        return text.strip()