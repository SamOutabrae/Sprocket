import discord
import toml
import logging
import importlib
import sys, os

from discord.ext import commands

def read_token():
  with open("token.txt", "r") as file:
    token = file.read().strip()
    if token == "" or token is None:
      raise ValueError("Invalid token. Please ensure a valid token is provided in token.txt.")
    return token

def import_file(filepath: str, module_name: str = "temp_module"):
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module
    else:
        raise ImportError(f"Could not import module from file: {filepath}")

def get_modules_mainfiles() -> list:
  """
    Returns a list of imported mainfiles
  """
  mainfiles = {}
  
  with open("modules.toml", "r") as file:
    modules = toml.load(file)
    if not modules:
      raise ValueError("No modules found. Please ensure the modules.toml file is correctly formatted.")

    for module in modules:
      try:
       mainfile = modules[module]["mainfile"]
       logging.debug(f"Found mainfile {mainfile} for {module}")

       mainfile_module = import_file("modules/" + mainfile)
       mainfiles[module] = mainfile_module
       logging.debug(f"Imported mainfile for {module} sucessfully.")
       
      except KeyError as e:
        logging.error(f"Module {module} does not contain necessary keys. Check the declaration in modules.toml.")
    
      except Exception as e:
        logging.error("An error occured while importing the mainfile.")

  return mainfiles

def get_intents(mainfiles: dict) -> discord.Intents:
  intents = discord.Intents.none()

  for name, module in mainfiles.items():
    try:
      if hasattr(module, "get_intents"):
        module_intents = module.get_intents()
        intents = intents + module_intents
        logging.debug(f"Found intents for {name}.")
    except:
      logging.error(f"Cound not find intents for {name}.")
  
  return intents

def load_cogs(mainfiles: dict, client: discord.Client) -> list:
  """
    Loads cogs from all modules.
  """
  for name, module in mainfiles.items():
    try:
      if hasattr(module, "get_cogs"):
        module_cogs = module.get_cogs(client)
        logging.debug(f"Found cogs for {name}.")
        for cog in module_cogs:
          client.add_cog(cog)
          logging.info("Loaded cog {cog.__name__} from {name}.")
    except:
      logging.error("Could not find cogs for {name}.")
  
  logging.info("All cogs loaded.")

def initialize_bot():
  token = read_token()
  
  module_mainfiles = get_modules_mainfiles()
  intents = get_intents(module_mainfiles)

  client = commands.Bot(intents=intents, command_prefix="!")

  load_cogs(module_mainfiles, client)

  client.run(token)
  
if __name__ == "__main__":
    initialize_bot()