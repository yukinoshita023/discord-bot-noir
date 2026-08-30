import discord
from discord.ext import commands
import json
import os
from config import WAKUSEI_TWITTER_THREAD_ID

DATA_FILE = "data/wakusei_jump.json"

def load_data() -> dict:
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)

def save_data(data: dict):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

class WakuseiJumpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🛸 わくせいへ着陸", style=discord.ButtonStyle.primary, custom_id="wakusei_jump_button")
    async def jump(self, interaction: discord.Interaction, button: discord.ui.Button):
        data = load_data()
        message_id = data.get(str(interaction.user.id))

        if not message_id:
            await interaction.response.send_message("わくせいtwitterでのあなたの投稿がまだ見つかりませんでした。", ephemeral=True)
            return

        jump_url = f"https://discord.com/channels/{interaction.guild_id}/{WAKUSEI_TWITTER_THREAD_ID}/{message_id}"
        await interaction.response.send_message(jump_url, ephemeral=True)

class WakuseiJump(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or message.channel.id != WAKUSEI_TWITTER_THREAD_ID:
            return

        data = load_data()
        data[str(message.author.id)] = message.id
        save_data(data)

async def setup(bot):
    bot.add_view(WakuseiJumpView())
    await bot.add_cog(WakuseiJump(bot))
