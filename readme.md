# Sprocket

Sprocket is a lightweight, modular Discord bot designed to make it easy to mix and match different components, providing a flexible foundation for building powerful bots without unnecessary complexity.

## Getting Started

### Prerequisites

To run Sprocket, you'll need:

- **Python 3.12** (recommended)
- **Pycord 2.6** (`pip install py-cord`)
- **toml** (`pip install toml`)

Additionally, you'll need a Discord bot token. Create a file named `token.txt` in the root directory of your project and paste your bot token into it.

### Installing a Module

Installing a module is simple. Just copy the module's directory into the `modules/` folder and add its entry to **modules.toml**.

For example, the core module's directory structure looks like this: 
```
modules/
└── core/
    └── core.py
```

The corresponding `modules.toml` entry looks like this.

```toml
[core]
mainfile = "core/core.py"
```

**Note:** The category name of the modules.toml **must** match the name of the directory.

If you're using a module written by someone else, they should provide you with the correct entry for `modules.toml`. If you're writing your own module, see **Writing Your Own Modules** below.

### Intents

Discord bots require certain permissions to function correctly, known as **intents**. Sprocket makes it easy to identify which privileged intents your bot needs.

To check which privileged intents are required, run:

```bash
python sprocket.py intents
```

This command will display any privileged intents that must be enabled in your bot's settings on the Discord Developer Portal.

### Running Sprocket

Once you've set up your token and installed the necessary packages, you can start the bot with:

```bash
python sprocket.py
```

After a moment, you should see a message indicating that the bot is online.

## Writing Your Own Modules

All modules should be placed in the `modules/` directory, each in its own folder named after the module. You can organize your module's files however you like, but each module should have **one and only one mainfile**. This mainfile is declared in `modules.toml`.

### Required Mainfile Functions

Each module mainfile must implement two functions:

#### get_intents() -> discord.Intents

Returns a `discord.Intents` object representing the intents your module requires.

#### get_cogs(client: commands.Bot, directory: str) -> list

Returns a list of instantiated cogs to be added to the bot. Client is the discord bot instance, and directory is the directory of the module.

You don't have to pass these parameters along to your cogs if they do not need them. 

### Example Module Mainfile (`core.py`):

```python
import discord
from discord.ext import commands

# Specify the intents for this module
def get_intents() -> discord.Intents:
    intents = discord.Intents.default()
    return intents

# Returns a list of cogs for this module
def get_cogs(client: commands.Bot, directory: str) -> list:
    return [Core(client)]
```

### Error Handling

By default, all errors will be dealt with by the global error handler in the core module. This handler will not run if you provide a command or cog specific error handler. See py-cord's error handling for more details. 