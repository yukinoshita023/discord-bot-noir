import discord
from discord.ext import commands, tasks
from datetime import datetime, timezone, timedelta, time as dtime
from pathlib import Path

JST = timezone(timedelta(hours=9))

class TimeSignal(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.hourly_chime.start()

    @tasks.loop(time=[dtime(h, 0, 0, tzinfo=JST) for h in range(24)])
    async def hourly_chime(self):
        vc: discord.VoiceClient | None = self.bot.voice.get_current_vc()
        if not (vc and vc.is_connected()):
            return

        now = datetime.now(JST)
        base_dir = Path(__file__).resolve().parents[1] / "audio"
        chime_path = base_dir / "時報2倍速.wav"
        hour_path = base_dir / f"{now.hour}時です.wav"

        if not chime_path.exists():
            print(f"[TimeSignal] ファイルが見つかりません: {chime_path}")
            return
        if not hour_path.exists():
            print(f"[TimeSignal] ファイルが見つかりません: {hour_path}")
            return

        from services.tts import play_wav
        await play_wav(self.bot, vc, str(chime_path))
        await play_wav(self.bot, vc, str(hour_path))

    def cog_unload(self):
        self.hourly_chime.cancel()

async def setup(bot):
    await bot.add_cog(TimeSignal(bot))