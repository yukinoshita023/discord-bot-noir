import discord
import os
import asyncio
from gtts import gTTS
import subprocess

VOICE_TMP_DIR = "voice_tmp"  # 一時音声ファイルの保存先

if not os.path.exists(VOICE_TMP_DIR):
    os.makedirs(VOICE_TMP_DIR)

async def play_tts(vc, text, speed=1.5):
    """gTTS で音声を生成して再生する"""
    tts = gTTS(text=text, lang="ja")
    filename = os.path.join(VOICE_TMP_DIR, "vc_announce.mp3")
    tts.save(filename)

    # 音声の速度を変更するために FFmpeg を使って音声を再エンコード
    temp_filename = os.path.join(VOICE_TMP_DIR, "vc_announce_temp.mp3")
    subprocess.run([
        'ffmpeg', '-i', filename, '-filter:a', f'atempo={speed}', temp_filename, '-loglevel', 'quiet',
    ])

    # 変換した音声を再生
    vc.play(discord.FFmpegPCMAudio(temp_filename), after=lambda e: os.remove(temp_filename))

    # 元のファイルは削除
    os.remove(filename)

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
                    await play_tts(vc, f"{display_name} さんが参加しました", speed=2.0)

            elif before.channel and bot.user in before.channel.members:
                vc = discord.utils.get(bot.voice_clients, guild=member.guild)
                if vc and vc.is_connected():
                    await play_tts(vc, f"{display_name} さんが退出しました", speed=2.0)
