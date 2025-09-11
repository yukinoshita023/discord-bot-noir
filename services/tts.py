import discord
import asyncio
import tempfile
import os
import edge_tts  # 追加
from services.audio_queue import AudioQueue

# 任意：日本語の音声。好みで変更可（例: ja-JP-NanamiNeural, ja-JP-AoiNeural, ja-JP-KeitaNeural など）
DEFAULT_VOICE = "ja-JP-NanamiNeural"

def speed_to_rate(speed: float) -> str:
    """
    speed(倍速)を edge-tts の rate(% 表現)に変換する簡易関数。
    1.0 = 0%, 2.0 ≒ +100%, 0.8 ≒ -20% のような線形換算。
    """
    pct = int((speed - 1.0) * 100)
    sign = "+" if pct >= 0 else ""
    return f"{sign}{pct}%"

async def synthesize(text: str, speed: float = 2.0, voice: str = DEFAULT_VOICE) -> str:
    """
    edge-tts で MP3 を生成してテンポラリに保存し、パスを返す。
    呼び出し側は返却パスを FFmpegPCMAudio に渡せばよい。
    """
    rate = speed_to_rate(speed)

    # 一時ファイルに保存（delete=False にして再生完了後に手で消す）
    fd, path = tempfile.mkstemp(prefix="tts_", suffix=".mp3")
    os.close(fd)  # Windows互換のため先にFDを閉じる

    communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate)
    await communicate.save(path)
    return path

async def play_file(vc: discord.VoiceClient, path: str):
    """
    FFmpegPCMAudio に MP3 を渡せば ffmpeg がデコードしてくれる。
    再生終了まで待ち、最後に一時ファイルを削除。
    """
    def after_play(err):
        if err:
            print("play error:", err)

    audio = discord.FFmpegPCMAudio(path)
    vc.play(audio, after=after_play)

    try:
        while vc.is_playing() or vc.is_paused():
            await asyncio.sleep(0.1)
    finally:
        try:
            os.remove(path)
        except OSError:
            pass

async def play_tts(bot, vc: discord.VoiceClient, text: str, speed: float = 2.0):
    """
    直列再生のために audio_queue に積む。
    """
    async def job():
        path = await synthesize(text, speed)
        await play_file(vc, path)

    await bot.audio_queue.enqueue(job())

async def play_wav(bot, vc: discord.VoiceClient, path: str):
    """
    既存のwav/mp3ファイルを削除せずに再生する。
    """
    async def job():
        def after_play(err):
            if err:
                print("play error:", err)

        audio = discord.FFmpegPCMAudio(path)
        vc.play(audio, after=after_play)

        while vc.is_playing() or vc.is_paused():
            await asyncio.sleep(0.1)

    await bot.audio_queue.enqueue(job())
