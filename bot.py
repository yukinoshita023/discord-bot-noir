import discord
from config import TOKEN
from commands import setup_commands
from voice_chat_reader import VoiceChatReader #文字読み上げ機能
# from time_signal import TimeSignal # 時報機能

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

class MyBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)
        self.voice_chat_reader = VoiceChatReader(self,speed=2.0) # VC速度はここで変える
        # self.time_signal = TimeSignal(self) # 時報機能

    async def setup_hook(self):
        await setup_commands(self)
        print("全コマンドを追加しました")

        await self.tree.sync()
        print("スラッシュコマンドを同期しました")

bot = MyBot()

@bot.event
async def on_ready():
    print(f"ログインしました: {bot.user}")

@bot.event
async def on_message(message):
    await bot.voice_chat_reader.on_message(message)

# @bot.event
# async def on_voice_state_update(member, before, after):
#     """ ボットのVC接続状態が変化したときに time_signal.py の処理を実行 """
#     await bot.time_signal.on_voice_state_update(member, before, after)

bot.run(TOKEN)