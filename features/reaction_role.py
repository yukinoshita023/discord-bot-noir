import discord
from discord.ext import commands
import json
import os

DATA_FILE = "data/reaction_roles.json"

def load_data() -> dict:
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)

class ReactionRole(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.user_id == self.bot.user.id:
            return
        await self._handle_reaction(payload, add=True)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if payload.user_id == self.bot.user.id:
            return
        await self._handle_reaction(payload, add=False)

    async def _handle_reaction(self, payload: discord.RawReactionActionEvent, add: bool):
        data = load_data()
        entry = data.get(str(payload.message_id))
        if not entry:
            return
        if str(payload.emoji) != entry["emoji"]:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return
        role = guild.get_role(entry["role_id"])
        if not role:
            return

        try:
            member = payload.member if add else await guild.fetch_member(payload.user_id)
            if not member:
                return
            if add:
                await member.add_roles(role)
            else:
                await member.remove_roles(role)
        except (discord.Forbidden, discord.HTTPException):
            pass

async def setup(bot):
    await bot.add_cog(ReactionRole(bot))
