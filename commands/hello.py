import discord
from config import ADMIN_ROLE_ID

def has_role(role_id):
    async def predicate(interaction: discord.Interaction):
        member = interaction.user
        role = discord.utils.get(member.roles, id=role_id)
        if role:
            return True
        else:
            await interaction.response.send_message("あなたにはこのコマンドを実行する権限がありません", ephemeral=True)
            return False
    return discord.app_commands.check(predicate)

async def setup(bot):
    
    @bot.tree.command(name="hello", description="このコマンドによってノワールの生存確認ができます")
    @has_role(ADMIN_ROLE_ID)
    async def hello(interaction: discord.Interaction):
        await interaction.response.send_message("職務遂行中です！")
