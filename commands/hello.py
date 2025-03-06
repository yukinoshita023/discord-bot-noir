import discord

async def setup(bot):
    
    @bot.tree.command(name="hello", description="このコマンドは「やっほー！」と返します")
    async def hello(interaction: discord.Interaction):
        await interaction.response.send_message("やっほー！")