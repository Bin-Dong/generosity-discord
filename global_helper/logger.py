class Logger():
    log_channel = None

    @staticmethod
    def set_log_channel(channel):
        Logger.log_channel = channel

    @staticmethod
    async def log(message: str):
        await Logger.log_channel.send(message)