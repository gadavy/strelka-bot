import logging
import requests

from telegram import ParseMode


class Job():

    def __init__(self, telegram_bot):
        self.tgb = telegram_bot
        self.tgb.job_queue.run_repeating(
            self._update_balance, interval=1800, first=10
        )

        self.tgb.job_queue.run_repeating(
            self._send_balance, interval=1800, first=20
        )

    def _update_balance(self, context):
        cards = self.tgb.data_base.get_all_strelka()

        for card in cards:
            CARD_TYPE_ID = '3ae427a1-0f17-4524-acb1-a3f50090a8f3'
            payload = {'cardnum': card, 'cardtypeid': CARD_TYPE_ID}

            try:
                r = requests.get("http://strelkacard.ru/api/cards/status/",
                                 params=payload)
                balance = r.json()
                result = balance["balance"] / 100

            except Exception as ex:
                logging.warning("Update balance error: {}".format(ex))

            else:
                self.tgb.data_base.update_strelka_balance(card, result)

    def _send_balance(self, context):
        users = self.tgb.data_base.get_users_low_balance()

        for user in users:
            t_id = user[0]
            name = user[1]
            card = user[2][-4::]
            balc = user[3]

            text = (
                "{}, на карте _№{}_\nосталось всего {} рубля."
                .format(name, card, balc)
            )

            context.bot.send_message(
                chat_id=t_id, text=text, parse_mode=ParseMode.MARKDOWN
            )
