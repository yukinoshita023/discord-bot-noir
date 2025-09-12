import discord

class VoiceService:
    def __init__(self, bot: discord.Client):
        self.bot = bot

    async def join_if_needed(self, channel_id: int):
        guild = self.bot.guilds[0]
        channel = guild.get_channel(channel_id)
        if not channel or not isinstance(channel, discord.VoiceChannel):
            return

        if guild.voice_client and guild.voice_client.is_connected():
            return

        await channel.connect()

    def get_current_vc(self) -> discord.VoiceClient | None:
        guild = self.bot.guilds[0]
        return guild.voice_client
