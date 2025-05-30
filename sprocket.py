import discord
import toml
import logging
import importlib
import sys, os

from discord.ext import bridge

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("sprocket.log", "w"),
        logging.StreamHandler()
    ]
)

def read_token():
  with open("token.txt", "r") as file:
    token = file.read().strip()
    if token == "" or token is None:
      raise ValueError("Invalid token. Please ensure a valid token is provided in token.txt.")
    return token

def get_module(module_name: str, submodule: str):

    # Mount the folder in sys.modules under a fake package name
    full_module_path = f"modules.{module_name}.{submodule}"  # e.g., modules.sprocket_hypixel.main

    # Make sure 'modules' is in sys.path
    modules_dir = os.path.abspath("modules")
    if modules_dir not in sys.path:
        sys.path.insert(0, modules_dir)

    return importlib.import_module(full_module_path)

def get_modules_mainfiles() -> list:
  """
    Returns a list of imported mainfiles
  """
  mainfiles = {}
  modules = None
  
  if os.path.exists("modules.toml"):
    with open("modules.toml", "r") as file:
      modules = toml.load(file)
      if not modules:
        raise ValueError("No modules found. Please ensure the modules.toml file is correctly formatted.")
  elif os.path.exists("modules_default.toml"):
    logging.warning("No modules.toml found. Using modules_default.toml instead.")
    with open("modules_default.toml", "r") as file:
      modules = toml.load(file)
      if not modules:
        raise ValueError("No modules found.")
  else:
    raise FileNotFoundError("No modules.toml found. Please create it.")

  for module in modules:
    try:
      directory = f"modules/{module}"
      mainfile_name = os.path.splitext(os.path.basename(modules[module]['mainfile']))[0]  # strips .py
      mainfile_module = get_module(module, mainfile_name)
      logging.debug(f"Found mainfile {mainfile_name} for {module}")

      mainfiles[module] = mainfile_module
      logging.debug(f"Imported mainfile for {module} sucessfully.")
      
    except KeyError as e:
      logging.error(f"Module {module} does not contain necessary keys. Check the declaration in modules.toml.")
  
    except Exception as e:
      logging.error(e)
      logging.error(f"An error occured while importing the mainfile: {module}.")
    
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
        directory = "modules/" + name
        module_cogs = module.get_cogs(client, directory)
        logging.debug(f"Found cogs for {name}.")
        for cog in module_cogs:
          client.add_cog(cog)
          logging.info("Loaded cog {cog.__name__} from {name}.")
    except Exception as e:
      logging.error(e)
      logging.error(f"Could not find cogs for {name}.")
    print(f"Loaded cogs for {name}.")
  
  logging.info("All cogs loaded.")

def initialize_bot():
  token = read_token()
  
  module_mainfiles = get_modules_mainfiles()
  intents = get_intents(module_mainfiles)

  client = bridge.Bot(intents=intents, command_prefix="!")

  load_cogs(module_mainfiles, client)

  client.run(token)

def check_privileged_intents(intents: discord.Intents) -> list:
    privileged_intents = {
        "guild_members": intents.members,
        "message_content": intents.message_content,
        "guild_presences": intents.presences,
    }

    required_privileges = [name for name, enabled in privileged_intents.items() if enabled]

    if required_privileges:
        print("The following privileged intents are enabled and will require explicit permission:")
        for intent in required_privileges:
            print(f" - {intent}")
    else:
        print("No privileged intents are enabled.")

    return required_privileges

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "intents":
      intents = get_intents(get_modules_mainfiles())
      check_privileged_intents(intents)
      exit(0)

    initialize_bot()