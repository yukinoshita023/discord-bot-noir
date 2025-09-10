import discord

class VoiceService:
    def __init__(self, bot: discord.Client):
        self.bot = bot

    async def join_if_needed(self, channel_id: int):
        guilds = list(self.bot.guilds)
        if not guilds:
            return
        guild = guilds[0]
        channel = guild.get_channel(channel_id)
        if not channel or not isinstance(channel, discord.VoiceChannel):
            return

        vc = discord.utils.get(self.bot.voice_clients, guild=guild)
        if vc and vc.is_connected():
            if vc.channel.id != channel_id:
                await vc.move_to(channel)
            return
        await channel.connect()

    def get_current_vc(self) -> discord.VoiceClient | None:
        if not self.bot.guilds:
            return None
        guild = self.bot.guilds[0]
        return discord.utils.get(self.bot.voice_clients, guild=guild)
