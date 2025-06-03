import asyncio
import discord
import os
from gtts import gTTS
import subprocess
import uuid

VOICE_TMP_DIR = "voice_tmp"
os.makedirs(VOICE_TMP_DIR, exist_ok=True)

class TTSPlayer:
    def __init__(self, vc):
        self.vc = vc
        self.queue = asyncio.Queue()
        self.worker_task = asyncio.create_task(self.worker())
        print("[TTSPlayer] 初期化完了")

    async def enqueue_tts(self, text, speed=1.5):
        print(f"[enqueue_tts] キューに追加: '{text}'（速度: {speed}）")
        await self.queue.put(('tts', text, speed))

    async def enqueue_file(self, filepaths: list):
        print(f"[enqueue_file] ファイルキューに追加: {filepaths}")
        await self.queue.put(('file', filepaths))

    async def worker(self):
        print("[worker] 音声再生ループ開始")
        while True:
            item = await self.queue.get()
            print(f"[worker] キュー取得: {item}")

            try:
                if item[0] == 'tts':
                    _, text, speed = item
                    await self._play_tts(text, speed)
                elif item[0] == 'file':
                    _, filepaths = item
                    await self._play_files(filepaths)
                else:
                    print(f"[worker] 未知のキュータイプ: {item[0]}")
            except Exception as e:
                print(f"[worker] 再生エラー: {e}")
            finally:
                self.queue.task_done()

    async def _play_tts(self, text, speed):
        if not (0.5 <= speed <= 2.0):
            print(f"[play_tts] 無効な速度指定: {speed}")
            return

        base = os.path.join(VOICE_TMP_DIR, f"{uuid.uuid4()}.mp3")
        temp = os.path.join(VOICE_TMP_DIR, f"{uuid.uuid4()}_out.mp3")

        try:
            print(f"[play_tts] TTSファイル生成中: {base}")
            tts = gTTS(text=text, lang="ja")
            tts.save(base)

            print(f"[play_tts] ffmpeg 変換開始（速度: {speed}）")
            subprocess.run(
                ['ffmpeg', '-i', base, '-filter:a', f'atempo={speed}', temp, '-y', '-loglevel', 'quiet'],
                check=True
            )

            await self._play_audio(temp)

        except subprocess.CalledProcessError as e:
            print(f"[play_tts] ffmpeg 実行失敗: {e}")
        except Exception as e:
            print(f"[play_tts] エラー: {e}")
        finally:
            if os.path.exists(base):
                os.remove(base)
            if os.path.exists(temp):
                os.remove(temp)

    async def _play_files(self, filepaths):
        for path in filepaths:
            print(f"[play_files] ファイル再生: {path}")
            await self._play_audio(path)

    async def _play_audio(self, filepath):
        if not self.vc:
            print("[play_audio] vcがNoneです")
            return
        if not self.vc.is_connected():
            print("[play_audio] vcが接続されていません")
            return
        if self.vc.is_playing():
            print("[play_audio] 再生中のためスキップ")
            return
        if not os.path.exists(filepath):
            print(f"[play_audio] ファイルが存在しません: {filepath}")
            return

        print(f"[play_audio] 再生開始: {filepath}")
        done = asyncio.Event()

        def after_play(error):
            if error:
                print(f"[play_audio] 再生中エラー: {error}")
            else:
                print("[play_audio] 再生完了")
            done.set()

        try:
            audio = discord.FFmpegPCMAudio(filepath)
            self.vc.play(audio, after=after_play)
            await done.wait()
        except Exception as e:
            print(f"[play_audio] vc.playエラー: {e}")
