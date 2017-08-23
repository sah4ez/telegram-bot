from telegram import ReplyKeyboardMarkup
import property


def start(bot, update):
    msg = "hello!"
    reply_keyboard = [[property.BT_SITE, property.BT_SALE], [property.BT_MORTGAGE]]

    update.message.reply_text(
        msg,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
