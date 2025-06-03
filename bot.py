import discord
from config import TOKEN, MEIBO_CHANNEL_ID
from config import VOICE_CHANNEL_ID
from commands import setup_commands
from voice_chat_reader import VoiceChatReader  # テキスト読み上げ機能
from time_signal import TimeSignal  # 時報機能
from meibo_reaction import ReactionHandler  # 名簿リアクション機能
import voice_state_announce  # 入退出読み上げ機能
from audio_queue import TTSPlayer  # 共通音声再生キュー

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

class MyBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)

        self.tts_player = None
        self.voice_chat_reader = None
        self.time_signal = None
        self.reaction_handler = ReactionHandler(self)

    async def setup_hook(self):
        await setup_commands(self)
        print("全コマンドを追加しました")

        await self.tree.sync()
        print("スラッシュコマンドを同期しました")

bot = MyBot()

@bot.event
async def on_ready():
    print(f"ログインしました: {bot.user}")

    vc = discord.utils.get(bot.voice_clients)
    if vc and vc.is_connected():
        print("ボイスチャンネルに接続済みです")
        bot.tts_player = TTSPlayer(vc)

        bot.voice_chat_reader = VoiceChatReader(bot, bot.tts_player, speed=2.0)
        bot.time_signal = TimeSignal(bot, bot.tts_player)
        voice_state_announce.setup(bot, bot.tts_player)

    else:
        print("ボイスチャンネルに接続していません（読み上げ機能をスキップ）")

@bot.event
async def on_message(message):
    if bot.voice_chat_reader:
        await bot.voice_chat_reader.on_message(message)

    if message.channel.id == MEIBO_CHANNEL_ID:
        await bot.reaction_handler.add_reactions(message)

bot.run(TOKEN)
