import discord
from discord.ext import commands

SLEEP_ROOM_NAME = "すやすや部屋"

class SleepRoom(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if member.bot or before.channel == after.channel:
            return

        if before.channel and before.channel.name == SLEEP_ROOM_NAME and len(before.channel.members) == 0:
            try:
                await before.channel.delete(reason="すやすや部屋が空になったため削除")
            except discord.HTTPException:
                pass

async def setup(bot):
    await bot.add_cog(SleepRoom(bot))
