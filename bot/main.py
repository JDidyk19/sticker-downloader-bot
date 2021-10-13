import telebot
from telebot.types import Message
from config import TOKEN

bot = telebot.TeleBot(TOKEN, parse_mode=None)


@bot.message_handler(commands=['start'])
def start(message: Message) -> None:
    bot.send_message(message.chat.id,
                     f'Hello! I\'m bot - @{bot.get_me().username}\n' +
                     f'Have a good day!!\n' +
                     f'I\'ll help you download stickers!\n' +
                     f'Send me a sticker and I\'ll download it for you')


if __name__ == '__main__':
    bot.polling()
