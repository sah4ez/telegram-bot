import numpy as np
import property
import bot_log

LOG = bot_log.get_logger('mortgage')


class Mortgage:
    def __init__(self, s=10000, p_year=12, T=12) -> None:
        self.price_apartment = s
        self.first_payment = 0
        self.p_year = p_year
        self.period = T
        self.coef = 12 * 100

    def payment(self):
        result = ((self.price_apartment - self.first_payment) * (self.p_year / self.coef)) \
                 / (1 - np.power((1 + self.p_year / self.coef), -1 * self.period))
        str_res = format("%.2f" % result)
        return float(str_res)


def cmd(bot, update, ids_state, ids_sum):
    msg = property.MORTGAGE_PHRASE_1
    chat_id = update.message.chat_id
    if chat_id not in ids_state.keys():
        ids_state[chat_id] = 2
        ids_sum[chat_id] = Mortgage()
        update.message.reply_text(msg)


def calc(bot, update, ids_state, ids_sum):
    chat_id = update.message.chat_id
    if chat_id not in ids_sum.keys() or chat_id not in ids_state.keys():
        return

    state = ids_state[chat_id]
    num = ids_sum[chat_id]
    if state == 2:
        update.message.reply_text(property.MORTGAGE_PHRASE_2)
        ids_state[chat_id] = 3
        ids_sum[chat_id].price_apartment = float(update.message.text)
    elif state == 3:
        update.message.reply_text(property.MORTGAGE_PHRASE_3)
        ids_state[chat_id] = 4
        ids_sum[chat_id].period = float(update.message.text)
    elif state == 4:
        state = 0
        ids_sum[chat_id].first_payment = float(update.message.text)

        update.message.reply_text(
            property.MORTGAGE_PHRASE_4 % (ids_sum[chat_id].payment(), ids_sum[chat_id].p_year))
        cancel(bot, update, ids_state, ids_sum)

    LOG.info("State: %s" % state)


def cancel(bot, update, ids_state, ids_sum):
    chat_id = update.message.chat_id
    del ids_state[chat_id]
    del ids_sum[chat_id]
    LOG.debug("State was: %d" % ids_state.__len__())
