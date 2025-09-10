import discord
from discord.ext import commands, tasks
from datetime import datetime, timezone, timedelta

JST = timezone(timedelta(hours=9))

class TimeSignal(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self._loop.start()

    @tasks.loop(minutes=1)
    async def _loop(self):
        now = datetime.now(JST)
        if now.minute == 0:  # 毎正時
            vc = self.bot.voice.get_current_vc()
            if vc and vc.is_connected():
                from services.tts import play_tts
                await play_tts(self.bot, vc, f"{now.hour}時になりました", speed=2.0)

    def cog_unload(self):
        self._loop.cancel()

async def setup(bot):
    await bot.add_cog(TimeSignal(bot))
