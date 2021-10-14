import telebot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import TOKEN

bot = telebot.TeleBot(TOKEN, parse_mode=None)


@bot.message_handler(commands=['start'])
def start(message: Message) -> None:
    bot.send_message(message.chat.id,
                     f'Hi! I\'m bot - @{bot.get_me().username}\n' +
                     f'Have a good day!!\n' +
                     f'I\'ll help you download stickers!\n' +
                     f'Send me a sticker and I\'ll download it for you')


@bot.message_handler(content_types=['text', 'sticker'])
def message(message: Message) -> None:
    if message.text:
        bot.send_message(message.chat.id, 'You need to send me a sticker‼')

    elif message.sticker:
        sticker_info = message.sticker
        inline_markup = InlineKeyboardMarkup(row_width=2).add(
            InlineKeyboardButton('Download the sticker', callback_data='sticker'),
            InlineKeyboardButton('Download sticker pack', callback_data='pack')
        )
        bot.send_message(message.chat.id,
                         f'Information about the sticker:\n' +
                         f'file id: {sticker_info.file_id}\n' +
                         f'emoji: {sticker_info.emoji}\n' +
                         f'set name: {sticker_info.set_name}', reply_markup=inline_markup)


if __name__ == '__main__':
    bot.polling()
