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
    @bot.tree.command(name="join", description="指定のボイスチャンネルに接続します")
    @has_role(ADMIN_ROLE_ID)
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