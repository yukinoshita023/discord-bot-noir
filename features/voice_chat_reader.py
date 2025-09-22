import re
import discord
from discord.ext import commands
from services.tts import play_tts
from config import VOICE_CHANNEL_ID

URL_RE = re.compile(r'https?://\S+|www\.\S+')

def replace_urls(text: str) -> str:
    return URL_RE.sub(" URL省略 ", text)

def cleaned_text_for_tts(raw: str, limit: int = 50) -> str:
    text = replace_urls(raw)
    text = " ".join(text.split())
    if len(text) > limit:
        text = text[:limit] + "以下略"
    return text

def is_in_target_voice_text_chat(message: discord.Message, target_vc_id: int) -> bool:
    ch = message.channel
    if isinstance(ch, discord.VoiceChannel):
        return ch.id == target_vc_id
    return False

class VoiceChatReader(commands.Cog):
    def __init__(self, bot: discord.Client, speed: float = 2.0):
        self.bot = bot
        self.speed = speed
        self.target_vc_id = VOICE_CHANNEL_ID

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Bot自身の発言は無視
        if message.author.bot:
            return

        # 対象VCのテキストチャット限定
        if not is_in_target_voice_text_chat(message, self.target_vc_id):
            return

        # Botと同じVCにメッセージ送信者が接続しているか
        vc = discord.utils.get(self.bot.voice_clients, guild=message.guild)
        member: discord.Member = message.author
        if not vc or not member.voice or member.voice.channel.id != vc.channel.id:
            return

        # セルフミュート中のユーザーのみ読み上げ
        vs = member.voice
        if not vs.self_mute:
            return

        text = cleaned_text_for_tts(message.content)
        if not text:
            return

        await play_tts(self.bot, vc, text, speed=self.speed)

async def setup(bot):
    await bot.add_cog(VoiceChatReader(bot, speed=1.7))
