import discord
import asyncio
from discord.ext import tasks
from discord import FFmpegPCMAudio

class TimeSignal:
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 905329383630340117  # 音声を流すチャンネルIDをここに設定
        self.audio_path = "audio/4時です.wav"  # 音声ファイルのパス
        self.play_signal.start()  # 時報タスクを開始

    @tasks.loop(minutes=1)
    async def play_signal(self):
        # 1分ごとに実行される処理
        channel = self.bot.get_channel(self.channel_id)
        
        if channel and isinstance(channel, discord.VoiceChannel):
            # ボイスチャンネルに接続していない場合
            voice_client = channel.guild.voice_client
            if voice_client is None:
                print("ボットは通話中ではありません。")
                return  # 通話に参加していなければ終了

            # ボイスチャンネルに接続済みの場合、音声を再生
            voice_client.play(FFmpegPCMAudio(self.audio_path), after=lambda e: print("音声再生終了"))
            print("音声を再生中...")
        else:
            print("指定したチャンネルが見つかりませんでした。")

    @play_signal.before_loop
    async def before_play_signal(self):
        # 最初に1分待機
        await asyncio.sleep(60)
