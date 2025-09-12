import discord
from discord.ext import commands
from services.tts import play_tts

class VoiceStateAnnounce(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.id == self.bot.user.id:
            return

        joined = after.channel and before.channel != after.channel
        left   = before.channel and before.channel != after.channel and not after.channel

        vc = discord.utils.get(self.bot.voice_clients, guild=member.guild)
        if not vc or not vc.is_connected():
            return

        if joined and self.bot.user in after.channel.members:
            await play_tts(self.bot, vc, f"{member.display_name} さんが参加しました", speed=2.0)

        if left and self.bot.user in before.channel.members:
            await play_tts(self.bot, vc, f"{member.display_name} さんが退出しました", speed=2.0)

async def setup(bot):
    await bot.add_cog(VoiceStateAnnounce(bot))