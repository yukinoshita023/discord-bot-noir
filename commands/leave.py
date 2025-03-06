import discord
from config import VOICE_CHANNEL_ID

async def setup(bot):
    @bot.tree.command(name="leave", description="指定のボイスチャンネルから切断します")
    async def leave(interaction: discord.Interaction):
        voice_client = interaction.guild.voice_client

        if voice_client is None:
            await interaction.response.send_message("ボイスチャンネルに接続していません。")
            return

        if voice_client.channel.id != VOICE_CHANNEL_ID:
            await interaction.response.send_message(f"指定されたボイスチャンネル（{VOICE_CHANNEL_ID}）には接続していません。")
            return

        await voice_client.disconnect()
        await interaction.response.send_message(f"{voice_client.channel.name} から切断しました。")
