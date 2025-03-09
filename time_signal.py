import discord
import asyncio
from discord.ext import tasks
from discord import FFmpegPCMAudio
from datetime import datetime
import pytz

class TimeSignal:
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 905329383630340117  # 音声を流すチャンネルIDをここに設定
        self.audio_path = "audio/4時です.wav"  # 音声ファイルのパス
        self.audio_path = "audio/"  # 音声ファイルのパスのプレフィックス
        self.play_signal.start()  # 時報タスクを開始

    @tasks.loop(minutes=1)
    async def play_signal(self):

        # 日本標準時 (JST) を取得
        jst = pytz.timezone('Asia/Tokyo')
        now = datetime.now(jst)

        # 分の下一桁を取得
        minute_last_digit = now.minute % 10

        # 音声ファイルのパスを設定
        audio_file = f"{self.audio_path}{minute_last_digit}時です.wav"

        # 1分ごとに実行される処理
        channel = self.bot.get_channel(self.channel_id)
        
        if channel and isinstance(channel, discord.VoiceChannel):
            # ボイスチャンネルに接続していない場合
            voice_client = channel.guild.voice_client
            if voice_client is None:
                print("ボットは通話中ではありません。")
                return  # 通話に参加していなければ終了

            # ボイスチャンネルに接続済みの場合、音声を再生
            voice_client.play(FFmpegPCMAudio(audio_file), after=lambda e: print(f"音声再生終了: {audio_file}"))
            print(f"{minute_last_digit}時です.wav を再生中...")
        else:
            print("指定したチャンネルが見つかりませんでした。")

    @play_signal.before_loop
    async def before_play_signal(self):
        # 最初に1分待機
        await asyncio.sleep(60)
