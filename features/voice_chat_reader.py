import re
import discord
from discord.ext import commands
from services.tts import play_tts

# --- フィルタ系ユーティリティ ---

URL_RE = re.compile(r'https?://\S+|www\.\S+', re.IGNORECASE)

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".heic", ".heif"}
VIDEO_EXTS = {".mp4", ".mov", ".mkv", ".webm", ".avi", ".m4v"}

def strip_urls(text: str) -> str:
    return URL_RE.sub("", text)

def is_image_or_video_attachment(att: discord.Attachment) -> bool:
    # content_type が来ればそれを優先
    if att.content_type:
        ct = att.content_type.lower()
        if ct.startswith("image/") or ct.startswith("video/"):
            return True
    # 拡張子で補完
    name_lower = att.filename.lower()
    return any(name_lower.endswith(ext) for ext in IMAGE_EXTS | VIDEO_EXTS)

def cleaned_text_for_tts(raw: str, limit: int = 200) -> str:
    # URLを除去 → 空白整形 → 長文カット
    text = strip_urls(raw)
    text = " ".join(text.split())  # 連続空白を1つに
    if len(text) > limit:
        text = text[:limit] + " ……（以下略）"
    return text


class VoiceChatReader(commands.Cog):
    def __init__(self, bot: discord.Client, speed: float = 2.0):
        self.bot = bot
        self.speed = speed

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Botの発言は無視
        if message.author.bot:
            return

        # 画像/動画添付があればスキップ
        if any(is_image_or_video_attachment(att) for att in message.attachments):
            return

        # BotがこのギルドでVCに接続しているか
        vc = discord.utils.get(self.bot.voice_clients, guild=message.guild)
        if not (vc and vc.is_connected()):
            return

        # 投稿者がVCに居るか
        member: discord.Member = message.author
        if not member.voice or not member.voice.channel:
            return

        # Botと同じVCか
        if vc.channel.id != member.voice.channel.id:
            return

        # ミュート中か（自分ミュート or サーバーミュート）
        vs = member.voice
        if not (vs.self_mute or vs.mute):
            return

        # テキスト整形（URLだけ除去）
        text = cleaned_text_for_tts(message.content)
        if not text:
            return  # 空なら読まない

        # 読み上げ
        await play_tts(self.bot, vc, text, speed=self.speed)


async def setup(bot):
    await bot.add_cog(VoiceChatReader(bot))
