import discord
from config import VOICE_CHANNEL_ID

async def join_voice_channel_if_needed(bot: discord.Client):
    guild = discord.utils.get(bot.guilds)
    if not guild:
        print("ギルドが取得できませんでした")
        return

    channel = guild.get_channel(VOICE_CHANNEL_ID)
    if not channel:
        print("VCが見つかりません")
        return

    if guild.voice_client and guild.voice_client.is_connected():
        return

    try:
        await channel.connect()
        print(f"{channel.name} に接続しました")
    except Exception as e:
        print(f"VC接続に失敗: {e}")
