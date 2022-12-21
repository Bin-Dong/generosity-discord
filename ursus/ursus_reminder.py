from dataclasses import dataclass
from datetime import date, datetime
from dateutil import tz
from discord.ext.commands import Bot

from ursus.data_objects.interval import Interval
from ursus.data_objects.ursus_config import UrsusConfig
from discord.abc import GuildChannel

from global_helper.logger import Logger

def is_it_ursus(intervals: list[Interval], time_format, timezone):
    time_now = datetime.now(timezone).time()

    for interval in intervals:
        start = datetime.strptime(interval.start_time, time_format).time()
        end = datetime.strptime(interval.end_time, time_format).time()
        if start < end:
            if time_now >= start and time_now <= end: 
                return True
        else: # Crosses midnight
            if time_now >= start or time_now <= end:
                return True

    return False

class UrsusReminder():
    @staticmethod
    async def run(ursusConfig: UrsusConfig, get_channel):
        is_ursus_golden_time = is_it_ursus(
            intervals = ursusConfig.intervals,
            time_format = ursusConfig.time_format, 
            timezone = tz.gettz(ursusConfig.time_zone)
        )

        channel: GuildChannel = get_channel(ursusConfig.voice_channel_id)
        
        ursus_time_channel_name = "It's 2X Ursus time! 🐻🍴"
        non_ursus_time_channel_name = "Normal Ursus ❌"
        
        if is_ursus_golden_time and channel.name != ursus_time_channel_name:
            await channel.edit(name=ursus_time_channel_name)
        elif not is_ursus_golden_time and channel.name != non_ursus_time_channel_name:
            await channel.edit(name=non_ursus_time_channel_name)