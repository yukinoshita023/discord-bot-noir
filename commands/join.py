import discord
from config import VOICE_CHANNEL_ID

async def setup(bot):
    @bot.tree.command(name="join", description="指定のボイスチャンネルに接続します")
    async def join(interaction: discord.Interaction):
        channel = interaction.guild.get_channel(VOICE_CHANNEL_ID)

        if channel is None:
            await interaction.response.send_message("指定されたボイスチャンネルが見つかりません。")
            return

        if interaction.guild.voice_client:
            await interaction.response.send_message(f"すでに {interaction.guild.voice_client.channel} に接続しています。")
            return

        await channel.connect()
        await interaction.response.send_message(f"{channel.name} に接続しました。")