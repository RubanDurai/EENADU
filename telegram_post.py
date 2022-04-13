import json

from telegram import Bot
import logging

logger = logging.getLogger(__name__)

class TelegramPoster:

    def __init__(self, config: str):
        t_config = json.loads(open(config).read())
        self.chan_id = t_config["chan_id"]
        self.bot_token = t_config["bot_token"]

        self.bot = Bot(self.bot_token)

    def post(self, file: str):
        self.bot.send_document(self.chan_id,
                            open(file, "rb").read(),
                            filename=file)