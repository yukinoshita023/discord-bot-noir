import discord
from config import VOICE_CHANNEL_ID
from config import ADMIN_ROLE_ID

def has_role(role_id):
    async def predicate(interaction: discord.Interaction):
        member = interaction.user
        # ユーザーが指定したロールを持っているかチェック
        role = discord.utils.get(member.roles, id=role_id)
        if role:
            return True
        else:
            await interaction.response.send_message("あなたにはこのコマンドを実行する権限がありません。", ephemeral=True)
            return False
    return discord.app_commands.check(predicate)

async def setup(bot):
    @bot.tree.command(name="leave", description="指定のボイスチャンネルから切断します")
    @has_role(ADMIN_ROLE_ID)
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
