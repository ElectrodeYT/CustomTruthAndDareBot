import os

import discord, json
from discord.ext import commands
from truthdare import TruthDareCog

if os.path.exists('config.json'):
    with open('config.json', 'r') as f:
        config = json.loads(f.read())
else:
    config = {}

if os.environ.get('BOT_TOKEN') is not None:
    config['botToken'] = os.environ['BOT_TOKEN']

if os.environ.get("BOT_PREFIX") is not None:
    config['prefix'] = os.environ['BOT_PREFIX']

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=config['prefix'], intents=intents)


@bot.event
async def on_ready():
    await bot.add_cog(TruthDareCog(bot))
    await bot.tree.sync()


def main():
    bot.run(config['botToken'])


if __name__ == '__main__':
    main()
