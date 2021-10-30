import re
import os
import shutil
from typing import List, Tuple

import grequests
import requests
import telebot
from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from config import TOKEN, BASE_DIR, STICKERS_DIR, URL

bot = telebot.TeleBot(TOKEN, parse_mode=None)


@bot.message_handler(commands=['start'])
def start(message: Message) -> None:
    """Send to user welcome message.

    :param message: Object Message.
    """
    bot.send_message(message.chat.id,
                     f'Hi! I\'m bot - @{bot.get_me().username}.\n' +
                     f'Have a good day!!\n' +
                     f'I\'ll help you download stickers!\n' +
                     f'Send me a sticker and I\'ll download it for you.')


@bot.message_handler(content_types=['text', 'sticker'])
def message(message: Message) -> None:
    """Send to user warning message or sticker information and a inline keyboard.

    :param message: Object Message.
    """
    if message.text:
        bot.send_message(message.chat.id, 'You need to send me a sticker.‼')

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
    sticker_info = get_sticker_data(call.message.text)
    bot.edit_message_reply_markup(chat_id, call.message.id, reply_markup=None)
    if call.data == 'sticker':
        sticker(sticker_info, chat_id)
    elif call.data == 'pack':
        sticker_pack(sticker_info, chat_id)


def sticker(sticker_info: dict, chat_id: str) -> None:
    """Handle the "sticker" button.
    Create a folder, download sticker, create archive file of folder.
    Send to user archive file and delete archive and folder.

    :param sticker_info: A dictionary with data sticker.
    :param chat_id: A user's id.
    """
    path_to_folder = create_folder(chat_id)
    file_id = sticker_info['file_id']
    file_path = bot.get_file(file_id).file_path
    file_name = file_path.split('/')[1]
    image = download_sticker(file_path)
    save_image(image, file_name, path_to_folder)
    # Folder archiving
    shutil.make_archive(base_name=path_to_folder, format='tar', root_dir=path_to_folder)
    with open(path_to_folder + '.tar', 'rb') as archive:
        bot.send_document(chat_id, archive)
    # Delete tar file and folder
    delete_folder_file(path_to_folder)


def sticker_pack(sticker_info: dict, chat_id: str) -> None:
    """Handle the "pack" button.
    Create a folder, asynchronous download of stickers, create archive file of folder.
    Send to user archive file and delete archive and folder.

    :param sticker_info: A dictionary with data sticker.
    :param chat_id: A user's id.
    """
    bot.send_message(chat_id, 'Please wait a moment😛')
    path_to_folder = create_folder(chat_id)
    set_name = sticker_info['set_name']
    sticker_list = bot.get_sticker_set(set_name).stickers
    tasks = []
    for sticker in sticker_list:
        file_path = bot.get_file(sticker.file_id).file_path
        file_name = file_path.split('/')[1]
        tasks.append((file_path, file_name))
    images = download_stickers(tasks)
    for name, image in images:
        save_image(image.content, name, path_to_folder)
    # Folder archiving
    shutil.make_archive(base_name=path_to_folder, format='tar', root_dir=path_to_folder)
    with open(path_to_folder + '.tar', 'rb') as archive:
        bot.send_document(chat_id, archive)
    # Delete tar file and folder
    delete_folder_file(path_to_folder)


def download_sticker(file_path: str) -> bytes:
    """Download one sticker from Telegram server.

    :param file_path: Path where the sticker is located.
    :return: Bytes of image.
    """
    response = requests.get(URL.format(TOKEN=TOKEN, file_path=file_path)).content
    return response


def download_stickers(tasks: List[Tuple]) -> List[Tuple]:
    """Asynchronous download of stickers from Telegram server.

    :param tasks: List of tuples with image name and path.
    :return: List of tuples image name and response
    """
    file_names = [task[1] for task in tasks]
    gen = (grequests.get(URL.format(TOKEN=TOKEN, file_path=task[0])) for task in tasks)
    response = grequests.map(gen)
    return list(zip(file_names, response))


def create_folder(chat_id: str) -> str:
    """Create folder for stickers.

    :param chat_id: A user's id.
    :return: Path to folder.
    """
    path = os.path.join(STICKERS_DIR, chat_id)
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def delete_folder_file(path: str) -> None:
    """Deleting archive file and folder with stickers.

    :param path: Path to folder.
    """
    # Delete archive file
    os.remove(path + '.tar')
    # Delete folder
    shutil.rmtree(path)


def save_image(image: bytes, image_name: str, path: str) -> None:
    """Save image to a user's folder.

    :param image: Bytes of image.
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
