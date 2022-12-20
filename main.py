from datetime import datetime, time, timedelta
import json
import os
from sys import prefix
import sys
import discord
from discord.ext.commands import Bot, Context
from discord.ext import commands, tasks
from dacite import from_dict

from ursus.ursus_reminder import UrsusReminder
from ursus.data_objects.ursus_config import UrsusConfig
from clock.clock import Clock

from global_helper.logger import Logger

from dateutil import tz

config_file = "config.json"
if len(sys.argv) > 1 and sys.argv[1] == "prod":
    config_file = "config.production.json"

if not os.path.isfile(config_file):
    sys.exit(f"{config_file} not found! Please add it and try again.")
else:
    with open(config_file) as file:
        config = json.load(file)

intents = discord.Intents.default()
intents.message_content = True

bot = Bot(command_prefix=commands.when_mentioned_or(
    config["prefix"]), intents=intents, help_command=None)


@bot.event
async def on_ready():
    # Logger.set_log_channel(bot.get_channel(config["log_channel_id"]))
    print(f'We have logged in as {bot.user}')
    
    if not ursus_reminder.is_running():
        ursus_reminder.start()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if int(message.author.id) in config["react_to_users"]:
        await message.add_reaction("🧋") # Bubble Tea Emoji
    
    await bot.process_commands(message)

@tasks.loop(minutes=5.0)
async def ursus_reminder():
    """Ursus Channel Reminder"""
    ursus_configuration = from_dict(data_class = UrsusConfig, data = config["ursus_time"])
    await UrsusReminder.run(ursus_configuration, bot.get_channel)

@bot.command(name="clock")
async def clock(ctx):
    await Clock.run(ctx.channel)

bot.run(config["token"])
