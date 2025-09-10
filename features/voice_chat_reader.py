import discord
from discord.ext import commands
from services.tts import play_tts

class VoiceChatReader(commands.Cog):
    def __init__(self, bot: discord.Client, speed: float = 2.0):
        self.bot = bot
        self.speed = speed

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        # チャンネルや条件は必要に応じて判定
        vc = discord.utils.get(self.bot.voice_clients, guild=message.guild)
        if vc and vc.is_connected():
            await play_tts(self.bot, vc, message.content, speed=self.speed)

async def setup(bot):
    await bot.add_cog(VoiceChatReader(bot))