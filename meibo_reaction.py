import discord

class ReactionHandler:
    def __init__(self, bot):
        self.bot = bot

    async def add_reactions(self, message):
        # ここでリアクションを追加する
        try:
            await message.add_reaction("👍")  # サムズアップ
            await message.add_reaction("❤️")  # ハート
            await message.add_reaction("🚀")  # 笑顔の顔
            print("リアクションを追加しました。")
        except Exception as e:
            print(f"リアクションの追加に失敗しました: {e}")