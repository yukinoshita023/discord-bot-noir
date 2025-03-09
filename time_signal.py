import discord
import asyncio
from discord.ext import tasks
from discord import FFmpegPCMAudio
from datetime import datetime, timedelta
import pytz
from config import VOICE_CHANNEL_ID

class TimeSignal:
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = VOICE_CHANNEL_ID  # 音声を流すチャンネルIDをここに設定
        self.audio_path = "audio/"  # 音声ファイルのパスのプレフィックス
        self.next_signal_time = None
        self.calculate_next_signal_time()  # 初回の時刻を計算して設定
        self.play_signal.start()  # 時報タスクを開始

    def calculate_next_signal_time(self):
        """次の時刻の切り替わりまでの待機時間を計算"""
        jst = pytz.timezone('Asia/Tokyo')
        now = datetime.now(jst)
        
        # 次の時刻の切り替わりまでの時間を計算（分が0になるタイミング）
        next_hour = (now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1))
        
        # 次の時報までの待機時間（秒）
        self.next_signal_time = next_hour - now
        print(f"次の時報まで待機時間: {self.next_signal_time}")

    @tasks.loop(seconds=1)
    async def play_signal(self):
        # 次の時報まで待機した後に音声を流す
        if self.next_signal_time.total_seconds() <= 0:
            # 日本標準時 (JST) を取得
            jst = pytz.timezone('Asia/Tokyo')
            now = datetime.now(jst)

            # 時間に対応する音声ファイルを選択
            audio_file = f"{self.audio_path}{now.hour}時です.wav"

            # 音声を流す処理
            channel = self.bot.get_channel(self.channel_id)
            
            if channel and isinstance(channel, discord.VoiceChannel):
                voice_client = channel.guild.voice_client
                if voice_client is None:
                    print("ボットは通話中ではありません。")
                    return  # 通話に参加していなければ終了

                # 音声再生
                voice_client.play(FFmpegPCMAudio(audio_file), after=lambda e: print(f"音声再生終了: {audio_file}"))
                print(f"{now.hour}時です.wav を再生中...")
            
            # 1時間待機して次の時報を流す
            self.calculate_next_signal_time()  # 次の時報までの待機時間を再計算

    @play_signal.before_loop
    async def before_play_signal(self):
        # 初回は次の時刻の切り替わりまで待機
        await asyncio.sleep(self.next_signal_time.total_seconds())