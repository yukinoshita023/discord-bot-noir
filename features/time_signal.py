import discord
from discord.ext import commands, tasks
from datetime import datetime, timezone, timedelta
from pathlib import Path

JST = timezone(timedelta(hours=9))

class TimeSignal(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self._loop.start()

    @tasks.loop(minutes=1)
    async def _loop(self):
        now = datetime.now(JST)
        if now.minute != 0:
            return

        vc: discord.VoiceClient | None = self.bot.voice.get_current_vc()
        if not (vc and vc.is_connected()):
            return

        # features/ の1つ上にある audio ディレクトリ
        base_dir = Path(__file__).resolve().parents[1] / "audio"
        chime_path = base_dir / "時報2倍速.wav"
        hour_path = base_dir / f"{now.hour}時です.wav"  # 0〜23時のファイルを参照

        if not chime_path.exists():
            print(f"[TimeSignal] ファイルが見つかりません: {chime_path}")
            return
        if not hour_path.exists():
            print(f"[TimeSignal] ファイルが見つかりません: {hour_path}")
            return

        # audio_queue 経由で順番に再生
        from services.tts import play_wav
        await play_wav(self.bot, vc, str(chime_path))
        await play_wav(self.bot, vc, str(hour_path))

    def cog_unload(self):
        self._loop.cancel()

async def setup(bot):
    await bot.add_cog(TimeSignal(bot))
