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
        self.calculate_next_signal_time() # 最初の時報までの時間を計算
        self.play_signal.start()

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

    async def play_audio_sequence(self, voice_client, files):
        """リストの音声ファイルを順番に再生"""
        if not files:
            return
        
        def after_play(error):
            if error:
                print(f"エラー発生: {error}")
            elif files:
                next_file = files.pop(0)
                print(f"再生中: {next_file}")
                voice_client.play(FFmpegPCMAudio(next_file), after=after_play)

        first_file = files.pop(0)
        print(f"再生中: {first_file}")
        voice_client.play(FFmpegPCMAudio(first_file), after=after_play)

    @tasks.loop(hours=1)
    async def play_signal(self):
        try:
            jst = pytz.timezone('Asia/Tokyo')
            now = datetime.now(jst)

            jiho_audio_file = "audio/時報2倍速.wav"

            audio_file = f"{self.audio_path}{now.hour}時です.wav"

            if not os.path.exists(audio_file):
                print(f"エラー: 音声ファイル {audio_file} が存在しません。")
                return

            channel = self.bot.get_channel(self.channel_id)
            if channel and isinstance(channel, discord.VoiceChannel):
                voice_client = channel.guild.voice_client
                if voice_client is None:
                    print("ボットは通話中ではありません。")
                    return

                await self.play_audio_sequence(voice_client, [jiho_audio_file, audio_file])

            self.calculate_next_signal_time()
        except Exception as e:
            print(f"エラーが発生しました: {e}")
    
    @play_signal.before_loop
    async def before_play_signal(self):
        """最初に待機時間を設定"""
        await asyncio.sleep(self.next_signal_time_seconds)
