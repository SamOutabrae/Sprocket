import discord
from discord.ext import commands

import logging

# All module mainfiles MUST define this function
# Tells sprocket what intents this module requires
def get_intents() -> discord.Intents:
  intents = discord.Intents.default()
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
    print("Bot is ready.")

  # Default error handler
  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    # Check if the command has a local error handler
    if hasattr(ctx.command, 'on_error'):
      # Let the command's local error handler handle it
      return

    # Check if the cog has a custom error handler
    cog = ctx.cog
    if cog:
      cog_method = getattr(cog, "cog_command_error", None)
      # Ensure it's not the base class method
      if cog_method and cog_method.__func__ is not commands.Cog.cog_command_error:
        return
  
    logging.error(error)
    logging.warning(f"Warning: '{ctx.command.qualified_name}' in the '{cog.__class__.__name__}' cog has no cog-specific error handler.")
