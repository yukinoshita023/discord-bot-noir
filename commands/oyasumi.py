import discord
from discord import app_commands
from config import SLEEP_LOG_CHANNEL_ID

SLEEP_ROOM_NAME = "すやすや部屋"

async def setup(bot):
    @bot.tree.command(name="oyasumi", description="通話中に寝てしまった人をすやすや部屋に移動します")
    @app_commands.describe(member="寝てしまった人")
    async def oyasumi(interaction: discord.Interaction, member: discord.Member):
        if not interaction.guild or not isinstance(interaction.user, discord.Member):
            await interaction.response.send_message("このコマンドはサーバー内でのみ使用できます。", ephemeral=True)
            return

        author_channel = interaction.user.voice.channel if interaction.user.voice else None
        target_channel = member.voice.channel if member.voice else None

        if not author_channel:
            await interaction.response.send_message("あなたがボイスチャンネルに参加していません。", ephemeral=True)
            return

        if not target_channel:
            await interaction.response.send_message(f"{member.display_name} さんはボイスチャンネルに参加していません。", ephemeral=True)
            return

        if author_channel != target_channel:
            await interaction.response.send_message("同じ通話に参加している人にのみ実行できます。", ephemeral=True)
            return

        category = target_channel.category
        sleep_room = discord.utils.get(
            category.voice_channels if category else interaction.guild.voice_channels,
            name=SLEEP_ROOM_NAME,
        )

        if sleep_room is None:
            try:
                sleep_room = await interaction.guild.create_voice_channel(
                    SLEEP_ROOM_NAME,
                    category=category,
                    overwrites={
                        interaction.guild.default_role: discord.PermissionOverwrite(speak=False),
                    },
                    reason=f"{interaction.user.display_name} が {member.display_name} を移動するため作成",
                )
            except discord.Forbidden:
                await interaction.response.send_message("すやすや部屋を作成する権限がありません。", ephemeral=True)
                return
        else:
            try:
                await sleep_room.set_permissions(interaction.guild.default_role, speak=False)
            except discord.Forbidden:
                pass

        try:
            await member.move_to(sleep_room, reason=f"{interaction.user.display_name} により {SLEEP_ROOM_NAME} に移動")
        except discord.HTTPException:
            await interaction.response.send_message("メンバーの移動に失敗しました。", ephemeral=True)
            return

        await interaction.response.send_message(f"💤 {member.display_name} さんを {SLEEP_ROOM_NAME} に送りました。", ephemeral=True)

        log_channel = interaction.guild.get_channel(SLEEP_LOG_CHANNEL_ID)
        if log_channel:
            try:
                await log_channel.send(
                    f"💤 {interaction.user.display_name} さんが {member.display_name} さんを "
                    f"「{target_channel.name}」から {SLEEP_ROOM_NAME} に移動しました。"
                )
            except discord.HTTPException:
                pass
