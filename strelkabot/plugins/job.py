import logging
import asyncio
import datetime

import aiohttp
from telegram import ParseMode
from strelkabot.utils import TelegramBotPlugin


class Job(TelegramBotPlugin):

    def __init__(self, telegram_bot):
        super().__init__(telegram_bot)

        self.tg.job_queue.run_repeating(self._update_balance,
                                        interval=1800,
                                        first=1)

        self.tg.job_queue.run_repeating(self._send_balance,
                                        interval=3600,
                                        first=180)

    def _send_balance(self, context):
        info = self.tg.db.select_user_balance()

        for data in info:
            name = data[1]
            card = data[2][-4::]
            balc = data[3] / 100

            msg = f"{name}, на карте _№{card}_\nосталось всего {balc} рубля."

            context.bot.send_message(chat_id=data[0],
                                     text=msg,
                                     parse_mode=ParseMode.MARKDOWN)

    def _update_balance(self, context):
        cards = self.tg.db.select_cards()
        data = asyncio.run(self.__session(cards))

        if self.tg.db.insert_balance(data) is not True:
            logging.warning("Update balance failed.")

    async def __session(self, cards):
        time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        tasks = []

        async with aiohttp.ClientSession() as session:
            for card in cards:
                task = asyncio.create_task(self.__request(session, card, time))
                tasks.append(task)

            return await asyncio.gather(*tasks)

    async def __request(self, session, card, time):
        # region strelkakard params
        url = "https://strelkacard.ru/api/cards/status/"
        payload = {
            "cardnum": card,
            "cardtypeid": "3ae427a1-0f17-4524-acb1-a3f50090a8f3"}
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "referer": "https://strelkacard.ru/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)",
            "x-csrftoken": "null",
            "x-requested-with": "XMLHttpRequest"
        }
        # endregion
        async with session.get(url, params=payload, headers=headers) as r:
            response = await r.json()

            data = (time, card, response["balance"], response["baserate"])

            return data
