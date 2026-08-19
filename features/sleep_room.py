import discord
from discord.ext import commands
from config import SLEEP_LOG_CHANNEL_ID

SLEEP_ROOM_NAME = "すやすや部屋"

class SleepRoom(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    async def _log(self, guild: discord.Guild, message: str):
        channel = guild.get_channel(SLEEP_LOG_CHANNEL_ID)
        if not channel:
            return
        try:
            await channel.send(message)
        except discord.HTTPException:
            pass

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if member.bot or before.channel == after.channel:
            return

        if after.channel and after.channel.name == SLEEP_ROOM_NAME:
            try:
                await member.edit(deafen=True)
            except discord.HTTPException:
                pass
            await self._log(member.guild, f"💤 {member.display_name} さんが {SLEEP_ROOM_NAME} に入室しました。")

        if before.channel and before.channel.name == SLEEP_ROOM_NAME:
            room = before.channel
            try:
                await member.edit(deafen=False)
            except discord.HTTPException:
                pass
            await self._log(member.guild, f"👋 {member.display_name} さんが {SLEEP_ROOM_NAME} から退出しました。")

            if len(room.members) == 0:
                try:
                    await room.delete(reason="すやすや部屋が空になったため削除")
                    category_name = room.category.name if room.category else "不明"
                    await self._log(member.guild, f"🗑️ 「{category_name}」の {SLEEP_ROOM_NAME} を削除しました。")
                except discord.HTTPException:
                    pass

async def setup(bot):
    await bot.add_cog(SleepRoom(bot))
