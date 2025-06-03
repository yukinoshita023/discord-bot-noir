import discord
from audio_queue import TTSPlayer

tts_player = None

def setup(bot):
    @bot.event
    async def on_ready():
        global tts_player
        vc = discord.utils.get(bot.voice_clients)
        if vc and vc.is_connected():
            tts_player = TTSPlayer(vc)
        else:
            print("VCに接続していないため、TTSPlayerを初期化できませんでした")

    @bot.event
    async def on_voice_state_update(member, before, after):
        global tts_player
        if not tts_player:
            return

        if before.channel != after.channel:
            display_name = member.display_name

            if after.channel and bot.user in after.channel.members:
                await tts_player.enqueue_tts(f"{display_name} さんが参加しました", speed=2.0)

            elif before.channel and bot.user in before.channel.members:
                await tts_player.enqueue_tts(f"{display_name} さんが退出しました", speed=2.0)
