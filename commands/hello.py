import discord
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
    
    @bot.tree.command(name="hello", description="このコマンドは「やっほー！」と返します")
    @has_role(ADMIN_ROLE_ID)
    async def hello(interaction: discord.Interaction):
        await interaction.response.send_message("やっほー！")
