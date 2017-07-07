from telegram import (LabeledPrice, ForceReply, ShippingOption, ReplyKeyboardMarkup, KeyboardButton,
                      InlineKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, RegexHandler, MessageHandler, ConversationHandler,
                          Filters, PreCheckoutQueryHandler, ShippingQueryHandler)
import sys
import logging
import property
import glob
import random

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("__main__")

ids_state = {}
ids_sum = {}


# properties = {
#     property.STATES: {ids_state},
#     property.NUMBERS: {ids_sum},
# }


def start(bot, update):
    msg = "hello!"
    reply_keyboard = [[property.SITE, property.SALE], [property.MORTGAGE]]

    update.message.reply_text(
        msg,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))


def help(bot, update):
    msg = "help.."
    update.message.reply_text(msg)


def site(bot, update):
    msg = property.URL
    update.message.reply_text(msg)


def sale(bot, update):
    msg = property.SALE_TEXT
    chat_id = update.message.chat_id
    path = find_photo()
    bot.send_photo(chat_id=chat_id, caption=msg, photo=open(path, 'rb'))
    # rep_msg_id = update.message.message_id
    # bot.send_photo(chat_id=chat_id, reply_to_message_id=rep_msg_id, caption=msg, photo=open(path, 'rb'))


def find_photo():
    list_photo = glob.glob('./pictures/*.jpg')
    el = random.randint(0, list_photo.__len__())
    return list_photo[el - 1]


def mortgage(bot, update):
    msg = property.MORTGAGE_PHRASE_1
    chat_id = update.message.chat_id
    states = ids_state
    if chat_id not in states.keys():
        states[chat_id] = 2
        ids_sum[chat_id] = [0, 0, 0]
        update.message.reply_text(msg)


def calc(bot, update):
    chat_id = update.message.chat_id
    if chat_id not in ids_sum.keys() or chat_id not in ids_state.keys():
        return

    state = ids_state[chat_id]
    num = ids_sum[chat_id]
    if state == 2:
        update.message.reply_text(property.MORTGAGE_PHRASE_2)
        ids_state[chat_id] = 3
        num[0] = int(update.message.text)
    elif state == 3:
        update.message.reply_text(property.MORTGAGE_PHRASE_3)
        ids_state[chat_id] = 4
        num[1] = int(update.message.text)
    elif state == 4:
        state = 0
        num[2] = int(update.message.text)
        percent = 0.12
        vsego = num[1] * num[2]
        perv_vznos = num[0] - vsego
        mes_vznos = num[2] * (1 + percent)

        update.message.reply_text(
            property.MORTGAGE_PHRASE_4 % (perv_vznos, mes_vznos, num[1], percent * 100))
        cancel(bot, update)

    print("state", state)


def cancel(bot, update):
    chat_id = update.message.chat_id
    del ids_state[chat_id]
    del ids_sum[chat_id]
    logger.debug(ids_state.__len__())


def error(bot, update, error_msg):
    logger.warning('Update "%s" caused error "%s"' % (update, error_msg))


def main(token):
    updater = Updater(token=token)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler(property.CMD_START, start))
    dp.add_handler(CommandHandler(property.CMD_HELP, help))

    dp.add_handler(RegexHandler(property.SITE, site))
    dp.add_handler(RegexHandler(property.SALE, sale))
    dp.add_handler(RegexHandler(property.MORTGAGE, mortgage))
    dp.add_handler(RegexHandler('[0-9]', calc))

    dp.add_handler(CommandHandler(property.CMD_SALE, sale))
    dp.add_handler(CommandHandler(property.CMD_SITE, site))
    dp.add_handler(CommandHandler(property.CMD_MORTGAGE, mortgage))
    dp.add_handler(CommandHandler(property.CMD_CANCEL, cancel))

    dp.add_error_handler(error)

    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main(sys.argv[1])
