import discord
import asyncio
from discord.ext import tasks
from discord import FFmpegPCMAudio
from datetime import datetime, timedelta
import pytz
import os
from config import VOICE_CHANNEL_ID

class TimeSignal:
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = VOICE_CHANNEL_ID
        self.audio_path = "audio/"
        self.next_signal_time = None
        self.calculate_next_signal_time()  # 最初の時報までの時間を計算
        self.play_signal.start()  # 時報ループを開始

    def calculate_next_signal_time(self):
        """次の時報の時刻を計算"""
        jst = pytz.timezone('Asia/Tokyo')
        now = datetime.now(jst)
        
        # 次の整った時刻（1時間単位）を設定
        next_hour = (now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1))
        
        # 次の時報までの残り時間
        self.next_signal_time = next_hour
        self.next_signal_time_seconds = (self.next_signal_time - now).total_seconds()
        print(f"次の時報までの待機時間: {self.next_signal_time_seconds}秒")

    @tasks.loop(hours=1)  # 1時間ごとに処理を実行
    async def play_signal(self):
        """時報音声を再生する処理"""
        try:
            # 日本標準時 (JST) を取得
            jst = pytz.timezone('Asia/Tokyo')
            now = datetime.now(jst)

            audio_file = f"{self.audio_path}{now.hour}時です.wav"

            if not os.path.exists(audio_file):
                print(f"エラー: 音声ファイル {audio_file} が存在しません。")
                return

            # ボイスチャンネルを取得
            channel = self.bot.get_channel(self.channel_id)
            if channel and isinstance(channel, discord.VoiceChannel):
                voice_client = channel.guild.voice_client
                if voice_client is None:
                    print("ボットは通話中ではありません。")
                    return

                # 音声再生
                voice_client.play(FFmpegPCMAudio(audio_file), after=lambda e: print(f"音声再生終了: {audio_file}"))
                print(f"{now.hour}時です.wav を再生中...")

            # 次の時報までの待機時間を再計算
            self.calculate_next_signal_time()
        except Exception as e:
            print(f"エラーが発生しました: {e}")
    
    @play_signal.before_loop
    async def before_play_signal(self):
        """最初に待機時間を設定"""
        await asyncio.sleep(self.next_signal_time_seconds)  # 最初の時報まで待機
