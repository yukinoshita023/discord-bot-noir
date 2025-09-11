import discord

class VoiceService:
    def __init__(self, bot: discord.Client):
        self.bot = bot

    async def join_if_needed(self, channel_id: int):
        guild = self.bot.guilds[0]  # 必ず1サーバーしかない前提
        channel = guild.get_channel(channel_id)
        if not channel or not isinstance(channel, discord.VoiceChannel):
            return

        # すでに接続していれば何もしない
        if guild.voice_client and guild.voice_client.is_connected():
            return

        # 未接続なら接続
        await channel.connect()

    def get_current_vc(self) -> discord.VoiceClient | None:
        guild = self.bot.guilds[0]  # 1サーバー前提
        return guild.voice_client
