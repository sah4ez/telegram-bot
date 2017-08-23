import glob
import random
import property


def sale(bot, update):
    msg = property.RSP_SALE_TEXT
    chat_id = update.message.chat_id
    path = find_photo()
    bot.send_photo(chat_id=chat_id, caption=msg, photo=open(path, 'rb'))
    # rep_msg_id = update.message.message_id
    # bot.send_photo(chat_id=chat_id, reply_to_message_id=rep_msg_id, caption=msg, photo=open(path, 'rb'))


def find_photo():
    list_photo = glob.glob('./pictures/*.jpg')
    el = random.randint(0, list_photo.__len__())
    return list_photo[el - 1]
