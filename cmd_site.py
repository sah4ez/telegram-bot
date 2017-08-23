import property


def site(bot, update):
    msg = property.RSP_URL
    update.message.reply_text(msg)
