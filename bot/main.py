import re
import requests
import os
import shutil

import telebot
from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from config import TOKEN, BASE_DIR, STICKERS_DIR

bot = telebot.TeleBot(TOKEN, parse_mode=None)


@bot.message_handler(commands=['start'])
def start(message: Message) -> None:
    """Send to user welcome message.

    :param message: Object Message.
    """
    bot.send_message(message.chat.id,
                     f'Hi! I\'m bot - @{bot.get_me().username}\n' +
                     f'Have a good day!!\n' +
                     f'I\'ll help you download stickers!\n' +
                     f'Send me a sticker and I\'ll download it for you')


@bot.message_handler(content_types=['text', 'sticker'])
def message(message: Message) -> None:
    """Send to user warning message or sticker information and a inline keyboard.

    :param message: Object Message.
    """
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
    """Handle keyboard buttons.

    :param call: CallbackQuery object.
    """
    chat_id = str(call.message.chat.id)
    message_text = call.message.text
    sticker_info = get_sticker_data(message_text)
    if call.data == 'sticker':
        sticker(sticker_info, chat_id)
    elif call.data == 'pack':
        sticker_pack(sticker_info, chat_id)


def sticker(sticker_info: dict, chat_id: str) -> None:
    path_to_folder = create_folder(chat_id)

    file_id = sticker_info['file_id']

    file_path = bot.get_file(file_id).file_path
    file_name = file_path.split('/')[1]

    image = download_sticker(file_path)
    save_image(image, file_name, path_to_folder)
    zipping_folder(path_to_folder, chat_id)


def sticker_pack(sticker_info: dict, chat_id: str) -> None:
    path_to_folder = create_folder(chat_id)
    set_name = sticker_info['set_name']
    sticker_list = bot.get_sticker_set(set_name).stickers
    for sticker in sticker_list:
        file_id = sticker.file_id
        file_path = bot.get_file(file_id).file_path
        file_name = file_path.split('/')[1]
        image = download_sticker(file_path)
        save_image(image, file_name, path_to_folder)


def download_sticker(file_path: str) -> bytes:
    """Download sticker from Telegram server.

    :param file_path: Path where the sticker is located.
    :return: Bytes of image.
    """
    URL = f'https://api.telegram.org/file/bot{TOKEN}/{file_path}'
    response = requests.get(URL).content
    return response


def create_folder(chat_id: str) -> None:
    """Create folder for stickers.

    :param chat_id: user id.
    :return: Path to folder.
    """
    path = os.path.join(STICKERS_DIR, chat_id)
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def zipping_folder(path: str, chat_id: str) -> None:
    path = os.path.join(STICKERS_DIR, chat_id)
    shutil.make_archive(chat_id, 'tar', root_dir=path)



def save_image(image: bytes, image_name: str, path: str) -> None:
    """Save image to a user's folder.

    :param image:
    :param image_name: A image name.
    :param path: A location to save the image.
    """
    with open(f'{path}/{image_name}', 'wb') as img:
        img.write(image)


def get_sticker_data(text: str) -> dict:
    """Get file_id, set_name from message.

    :param text: Text message.
    :return: A dictionary with data sticker.
    """
    data = dict()
    file_id = re.search(r'file id: ([a-zA-Z0-9_-]+)', text).group(1)
    set_name = re.search(r'set name: ([a-zA-Z0-9_-]+)', text).group(1)
    data['file_id'] = file_id
    data['set_name'] = set_name
    return data


if __name__ == '__main__':
    bot.polling(none_stop=True)
