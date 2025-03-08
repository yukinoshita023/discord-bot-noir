import discord
import asyncio
import os
import re
from gtts import gTTS

class VoiceChatReader:
    def __init__(self, bot, speed=1.5):  # デフォルト速度を1.5倍に設定
        self.bot = bot
        self.speed = speed  # 再生速度を設定
        self.voice_tmp_dir = os.path.join(os.path.dirname(__file__), "voice_tmp")

    async def on_message(self, message):
        """ ユーザーがミュート中ならメッセージをVCで読み上げる """
        if message.author.bot:
            return  # ボットのメッセージは無視

        # 画像や動画が添付されている場合は無視
        if any(attachment.content_type and attachment.content_type.startswith(("image/", "video/")) for attachment in message.attachments):
            return

        # ボットがVCに接続しているか確認
        vc = discord.utils.get(self.bot.voice_clients, guild=message.guild)
        if vc and vc.is_connected():  # ボットがVCに接続している場合
            member = message.guild.get_member(message.author.id)
            if member and member.voice:  # ユーザーがボイスチャンネルに参加しているか確認
                # 同じボイスチャンネルにいるかチェック
                if member.voice.channel == vc.channel:
                    # ミュートされているか確認
                    if member.voice.self_mute or member.voice.mute:
                        text = self.filter_message(message.content)
                        if text:  # 空のメッセージは読み上げない
                            await self.read_text_in_vc(vc, text)

    def filter_message(self, text):
        """ メッセージ内のURLを検出して 'URL省略' に置き換え、絵文字を無視 """
        # 絵文字を取り除くための正規表現
        emoji_pattern = re.compile(r'<:.+?:\d+>|<a:.+?:\d+>|[\U00010000-\U0010ffff]')
        # URLを取り除くための正規表現
        url_pattern = re.compile(r'https?://\S+|www\.\S+')

        # 絵文字とURLを取り除く
        text = emoji_pattern.sub('', text)
        if url_pattern.search(text):  # URLが含まれていたら置き換え
            text = "URL省略"

        return text.strip()

    async def read_text_in_vc(self, vc, text):
        """ メッセージを音声に変換してVCで再生 """
        tts = gTTS(text=text, lang="ja")
        filename = os.path.join(self.voice_tmp_dir, "speech.mp3")
        tts.save(filename)

        # FFmpeg のフィルタを使って再生速度を変更
        ffmpeg_options = f'-filter:a "atempo={self.speed}"'

        vc.play(discord.FFmpegPCMAudio(filename, options=ffmpeg_options), after=lambda e: os.remove(filename))
        while vc.is_playing():
            await asyncio.sleep(1)
