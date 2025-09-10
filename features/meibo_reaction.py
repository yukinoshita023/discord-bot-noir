import discord
from discord.ext import commands
from config import MEIBO_CHANNEL_ID

class MeiboReaction(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if message.channel.id != MEIBO_CHANNEL_ID:
            return
        try:
            await message.add_reaction("👍")
            await message.add_reaction("❤️")
            await message.add_reaction("🚀")
        except discord.Forbidden:
            pass

async def setup(bot):
    await bot.add_cog(MeiboReaction(bot))
