import discord
from discord import app_commands
from features.wakusei_jump import WakuseiJumpView
from commands.create_reaction_role import has_admin_role

async def setup(bot):
    @bot.tree.command(name="wakusei_jump_setup", description="わくせい着陸ボタンをこのチャンネルに設置します")
    @has_admin_role()
    async def wakusei_jump_setup(interaction: discord.Interaction):
        await interaction.channel.send(
            "🛸 ボタンを押すと、わくせいtwitterでのあなたの最新の投稿にジャンプできます。",
            view=WakuseiJumpView(),
        )
        await interaction.response.send_message("設置しました。", ephemeral=True)

    @wakusei_jump_setup.error
    async def wakusei_jump_setup_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message(str(error), ephemeral=True)
