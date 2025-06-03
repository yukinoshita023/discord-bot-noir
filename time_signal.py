import discord
import asyncio
from discord.ext import tasks
from datetime import datetime, timedelta
import pytz
import os
from config import VOICE_CHANNEL_ID
from audio_queue import TTSPlayer

class TimeSignal:
    def __init__(self, bot, tts_player: TTSPlayer):
        self.bot = bot
        self.tts_player = tts_player
        self.channel_id = VOICE_CHANNEL_ID
        self.audio_path = "audio/"
        self.next_signal_time = None

        self.calculate_next_signal_time()
        self.play_signal.start()

    def calculate_next_signal_time(self):
        jst = pytz.timezone('Asia/Tokyo')
        now = datetime.now(jst)

        next_hour = (now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1))

        self.next_signal_time = next_hour
        self.next_signal_time_seconds = (self.next_signal_time - now).total_seconds()
        print(f"次の時報までの待機時間: {self.next_signal_time_seconds:.2f}秒")

    @tasks.loop(hours=1)
    async def play_signal(self):
        try:
            jst = pytz.timezone('Asia/Tokyo')
            now = datetime.now(jst)

            jiho_audio_file = os.path.join(self.audio_path, "時報2倍速.wav")
            hour_audio_file = os.path.join(self.audio_path, f"{now.hour}時です.wav")

            if not os.path.exists(hour_audio_file):
                print(f"エラー: 音声ファイル {hour_audio_file} が存在しません。")
                return

            if self.tts_player:
                await self.tts_player.enqueue_file([jiho_audio_file, hour_audio_file])
            else:
                print("TTSPlayerが初期化されていません")

            self.calculate_next_signal_time()

        except Exception as e:
            print(f"エラーが発生しました: {e}")

    @play_signal.before_loop
    async def before_play_signal(self):
        await asyncio.sleep(self.next_signal_time_seconds)
