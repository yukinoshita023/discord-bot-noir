import discord

class ReactionHandler:
    def __init__(self, bot):
        self.bot = bot

    async def add_reactions(self, message):
        try:
            await message.add_reaction("👍")
            await message.add_reaction("❤️")
            await message.add_reaction("🚀")
            print("リアクションを追加しました")
        except Exception as e:
            print(f"リアクションの追加に失敗しました: {e}")