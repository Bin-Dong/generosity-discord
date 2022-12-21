from dataclasses import dataclass
from datetime import date, datetime
import pytz
from pytz import timezone

from discord.ext.commands import Bot
from discord.abc import GuildChannel
import discord

from global_helper.logger import Logger

# To get abbreviation to zone name
# import collections
# import datetime as DT
# import pytz

# tzones = collections.defaultdict(set)
# abbrevs = collections.defaultdict(set)

# for name in pytz.all_timezones:
#     tzone = pytz.timezone(name)
#     for utcoffset, dstoffset, tzabbrev in getattr(
#             tzone, '_transition_info', [[None, None, DT.datetime.now(tzone).tzname()]]):
#         tzones[tzabbrev].add(name)
#         abbrevs[name].add(tzabbrev)

# tzones['PST']

class Clock():
    @staticmethod
    async def run(channel_to_reply):
        embed = discord.Embed(title="Clock 🕑", description="Here are the different times in their respective timezones:", color=0x00ff00)

        list_of_timezones = [
            "UTC", 
            "America/New_York", # EST/EDT 
            "America/Los_Angeles", # PST/PDT
            "US/Central", # CST/CDT
            "Europe/Gibraltar", # CEST 
            "Australia/Sydney", # AEST
            ]

        for zone in list_of_timezones:
            tzinfo = timezone(zone)
            time = datetime.now(tzinfo)
            timezone_abbreviation = time.strftime("%Z")
            time_formatted = time.strftime("%I:%M %p")
            embed.add_field(name=timezone_abbreviation, value = time_formatted, inline=False)

        await channel_to_reply.send(embed=embed)