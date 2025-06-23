import discord
from config import TOKEN, MEIBO_CHANNEL_ID, VOICE_CHANNEL_ID
from commands import setup_commands
from voice_chat_reader import VoiceChatReader
from time_signal import TimeSignal
from meibo_reaction import ReactionHandler
from voice_state_announce import play_tts
from audio_queue import AudioQueue
from vc_reconnect import join_voice_channel_if_needed

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

class MyBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)
        self.audio_queue = AudioQueue()
        self.voice_chat_reader = VoiceChatReader(self, speed=2.0)
        self.time_signal = None
        self.reaction_handler = ReactionHandler(self)

    async def setup_hook(self):
        await setup_commands(self)
        print("全コマンドを追加しました")
        await self.tree.sync()
        print("スラッシュコマンドを同期しました")
        self.time_signal = TimeSignal(self)

bot = MyBot()

@bot.event
async def on_ready():
    print(f"ログインしました: {bot.user}")
    await join_voice_channel_if_needed(bot)

@bot.event
async def on_voice_state_update(member, before, after):
    if member.id == bot.user.id and before.channel and after.channel is None:
        print("Botが通話から落ちました、再接続します")
        await join_voice_channel_if_needed(bot)
        return

    if before.channel != after.channel and member.id != bot.user.id:
        display_name = member.display_name
        vc = discord.utils.get(bot.voice_clients, guild=member.guild)

        if after.channel and bot.user in after.channel.members:
            if vc and vc.is_connected():
                await play_tts(bot, vc, f"{display_name} さんが参加しました", speed=2.0)

        elif before.channel and bot.user in before.channel.members:
            if vc and vc.is_connected():
                await play_tts(bot, vc, f"{display_name} さんが退出しました", speed=2.0)

@bot.event
async def on_message(message):
    await bot.voice_chat_reader.on_message(message)

    if message.channel.id == MEIBO_CHANNEL_ID:
        await bot.reaction_handler.add_reactions(message)

bot.run(TOKEN)