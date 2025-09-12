import discord
from discord.ext import commands
from config import TOKEN
from services.audio_queue import AudioQueue
from services.voice import VoiceService
from commands import setup_commands

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
        self.audio_queue = AudioQueue()
        self.voice = VoiceService(self)

    async def setup_hook(self):
        await setup_commands(self)
        
        await self.load_extension("features.voice_state_announce")
        await self.load_extension("features.voice_chat_reader")
        await self.load_extension("features.time_signal")
        await self.load_extension("features.meibo_reaction")
        await self.load_extension("features.vc_watchdog")

        await self.tree.sync()

bot = MyBot()

@bot.event
async def on_ready():
    print(f"ログインしました: {bot.user}")

bot.run(TOKEN)
