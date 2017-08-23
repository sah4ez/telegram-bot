import sys
from os import environ as env

from telegram.ext import (Updater, CommandHandler, RegexHandler)

import bot_log
import cmd_help
import cmd_sale
import cmd_site
import cmd_start
import mortgage as m
import property

LOG = bot_log.get_logger("main")
mortgage = m.Mortgage()
ids_state = {}
ids_sum = {}

TOKEN = env.get("TOKEN_BOT")
if TOKEN is None:
    TOKEN = sys.argv[1]
LOG.info('Token is loaded: %s' % TOKEN is not None)


def cmd_mortgage(bot, updater):
    m.cmd(bot, update=updater, ids_state=ids_state, ids_sum=ids_sum)


def cmd_calc(bot, updater):
    m.calc(bot, update=updater, ids_state=ids_state, ids_sum=ids_sum)


def cmd_cancel(bot, updater):
    m.cancel(bot, update=updater, ids_state=ids_state, ids_sum=ids_sum)


def error(bot, update, error_msg):
    LOG.warning('Update "%s" caused error "%s"' % (update, error_msg))


def main():
    updater = Updater(token=TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler(property.CMD_START, cmd_start.start))
    dp.add_handler(CommandHandler(property.CMD_HELP, cmd_help.help))

    dp.add_handler(RegexHandler(property.BT_SITE, cmd_site.site))
    dp.add_handler(CommandHandler(property.CMD_SITE, cmd_site.site))

    dp.add_handler(RegexHandler(property.BT_SALE, cmd_sale.sale))
    dp.add_handler(CommandHandler(property.CMD_SALE, cmd_sale.sale))

    dp.add_handler(RegexHandler(property.BT_MORTGAGE, cmd_mortgage))
    dp.add_handler(RegexHandler('[0-9]', cmd_calc))
    dp.add_handler(CommandHandler(property.CMD_MORTGAGE, cmd_mortgage))

    dp.add_handler(CommandHandler(property.CMD_CANCEL, cmd_cancel))

    dp.add_error_handler(error)

    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
