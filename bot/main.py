import telebot
from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from config import TOKEN
import re
import requests

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


@bot.callback_query_handler(func=lambda call: True)
def callback(call: CallbackQuery) -> None:
    sticker_info = get_sticker_data(call.message.text)
    if call.data == 'sticker':
        sticker(sticker_info)
    elif call.data == 'pack':
        sticker_pack(sticker_info)


def sticker(sticker_info: dict) -> None:
    file_id = sticker_info['file_id']
    file_path = bot.get_file(file_id).file_path
    image = download_sticker(file_path)


def sticker_pack(sticker_info: dict) -> None:
    set_name = sticker_info['set_name']
    sticker_list = bot.get_sticker_set(set_name).stickers
    for sticker in sticker_list[:5]:
        file_id = sticker.file_id
        file_path = bot.get_file(file_id).file_path
        image = download_sticker(file_path)


def download_sticker(file_path: str) -> bytes:
    '''
        Download sticker from Telegram server.
    '''
    URL = f'http://api.telegram.org/file/bot{TOKEN}/{file_path}'
    response = requests.get(URL).content
    return response


def get_sticker_data(text: str) -> dict:
    data = dict()
    file_id = re.search(r'file id: ([a-zA-Z0-9_-]+)', text).group(1)
    set_name = re.search(r'set name: ([a-zA-Z0-9_-]+)', text).group(1)
    data['file_id'] = file_id
    data['set_name'] = set_name
    return data


if __name__ == '__main__':
    bot.polling()
