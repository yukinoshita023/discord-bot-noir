import discord
import os
import asyncio
from gtts import gTTS

VOICE_TMP_DIR = "voice_tmp"  # 一時音声ファイルの保存先

if not os.path.exists(VOICE_TMP_DIR):
    os.makedirs(VOICE_TMP_DIR)

async def play_tts(vc, text):
    """gTTS で音声を生成して再生する"""
    tts = gTTS(text=text, lang="ja")
    filename = os.path.join(VOICE_TMP_DIR, "vc_announce.mp3")
    tts.save(filename)

    vc.play(discord.FFmpegPCMAudio(filename), after=lambda e: os.remove(filename))

def setup(bot):
    """ボットにイベントリスナーを追加"""
    @bot.event
    async def on_voice_state_update(member, before, after):
        if before.channel != after.channel:
            # ニックネーム（あれば）を取得、なければデフォルトのユーザー名
            display_name = member.display_name  

            vc = None
            if after.channel and bot.user in after.channel.members:
                vc = discord.utils.get(bot.voice_clients, guild=member.guild)
                if vc and vc.is_connected():
                    await play_tts(vc, f"{display_name} さんが参加しました")

            elif before.channel and bot.user in before.channel.members:
                vc = discord.utils.get(bot.voice_clients, guild=member.guild)
                if vc and vc.is_connected():
                    await play_tts(vc, f"{display_name} さんが退出しました")
