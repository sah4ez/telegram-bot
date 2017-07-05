from telegram import (LabeledPrice, ShippingOption, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, RegexHandler, MessageHandler, ConversationHandler,
                          Filters, PreCheckoutQueryHandler, ShippingQueryHandler)
import sys
import logging
import property
import glob
import random

logging.basicConfig(filename=property.LOG_FILE, level=logging.DEBUG)

logger = logging.getLogger("__main__")


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
    msg = "ipoteka-ipoteka"
    update.message.reply_text(msg)
    price1(bot=bot, update=update)
    price2(bot=bot, update=update)


def price1(bot, update):
    print('1')


def price2(bot, update):
    print('2')


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

    dp.add_handler(CommandHandler(property.CMD_SALE, sale))
    dp.add_handler(CommandHandler(property.CMD_SITE, site))
    dp.add_handler(CommandHandler(property.CMD_MORTGAGE, mortgage))

    dp.add_error_handler(error)

    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main(sys.argv[1])
