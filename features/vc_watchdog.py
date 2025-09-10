import discord
from discord.ext import commands
from config import VOICE_CHANNEL_ID

class VCWatchdog(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.voice.join_if_needed(VOICE_CHANNEL_ID)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.id == self.bot.user.id and before.channel and after.channel is None:
            await self.bot.voice.join_if_needed(VOICE_CHANNEL_ID)

async def setup(bot):
    await bot.add_cog(VCWatchdog(bot))
