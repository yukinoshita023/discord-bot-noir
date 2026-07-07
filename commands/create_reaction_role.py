import discord
from discord import app_commands
import json
import os
from config import ADMIN_ROLE_ID

DATA_FILE = "data/reaction_roles.json"

def load_data() -> dict:
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)

def save_data(data: dict):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def has_admin_role():
    async def predicate(interaction: discord.Interaction) -> bool:
        if not interaction.guild:
            raise app_commands.CheckFailure("このコマンドはサーバー内でのみ使用できます。")
        if not any(r.id == ADMIN_ROLE_ID for r in interaction.user.roles):
            raise app_commands.CheckFailure("このコマンドは「管理課」ロールを持つユーザーのみ使用できます。")
        return True
    return app_commands.check(predicate)

async def setup(bot):
    @bot.tree.command(name="create_reaction_role", description="リアクションでロールを付与するメッセージを作成します")
    @app_commands.describe(
        text="送信するメッセージのテキスト（改行は\\nで入力）",
        role="リアクションで付与するロール",
        emoji="リアクションに使う絵文字",
    )
    @has_admin_role()
    async def create_reaction_role(
        interaction: discord.Interaction,
        text: str,
        role: discord.Role,
        emoji: str,
    ):
        await interaction.response.defer(ephemeral=True)

        formatted_text = text.replace("\\n", "\n")

        try:
            msg = await interaction.channel.send(formatted_text)
            await msg.add_reaction(emoji)
        except discord.HTTPException:
            await interaction.followup.send("絵文字が無効です。Unicode絵文字を使用してください。", ephemeral=True)
            return

        data = load_data()
        data[str(msg.id)] = {"emoji": emoji, "role_ids": [role.id], "guild_id": interaction.guild_id}
        save_data(data)

        await interaction.followup.send(
            f"リアクションロールを作成しました！\n"
            f"絵文字: {emoji} → ロール: {role.mention}",
            ephemeral=True
        )

    @create_reaction_role.error
    async def create_reaction_role_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message(str(error), ephemeral=True)
