import discord
from discord.ext import commands

import logging

# All module mainfiles MUST define this function
# Tells sproket what intents this module requires
def get_intents() -> discord.Intents:
    intents = discord.Intents.default()
    intents.message_content = True
    
    return intents

# All module mainfiles MUST define this function
# Returns a list of cogs for the bot to load
def get_cogs(client: commands.Bot) -> list:

    return [
        Core(client)
    ]

class Core(commands.Cog):
    def __init__(self, client):
        self.client = client 
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.sync_commands()
        logging.info("Commands synced. Bot is ready.")

    @commands.slash_command()
    async def ping(self, ctx: discord.ApplicationContext):
        await ctx.respond("Pong!")
