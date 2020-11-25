import secret
import asyncio
import os
from telethon import TelegramClient, events
from telethon import utils
from dotenv import load_dotenv
 
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN') 
API_ID = os.getenv('API_ID') 
API_HASH = os.getenv('API_HASH')


bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)


@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    """Send a message when the command /start is issued."""
    await event.respond('Привет. Я просто учусь делать ботов, ничего интересного')
    raise events.StopPropagation


@bot.on(events.NewMessage(pattern='/admin'))
async def admin(event):
    await event.respond('''Такс, открыт секретный режим этого бота.
    Он умеет помещать в обычные сообщения зашифрованные послания с помощью невидимых символов.
    Команда /encode - создать секретное сообщение
    Команда /decode - расшифровать чужое секретное сообщение''')
    raise events.StopPropagation


@bot.on(events.NewMessage(pattern='/encode'))
async def do_encode(event):
    async with bot.conversation(event.chat_id) as conv:
        await conv.send_message('Сейчас создадим секретное сообщение. Введи основной текст, что-то обычное и не подозрительное. Это будет текст-прикрытие')
        cover_message = (await conv.get_response()).raw_text
        await conv.send_message('А теперь введи секретный текст')
        secret_message = (await conv.get_response()).raw_text
        while not any(x.isalpha() for x in secret_message):
            await conv.send_message("Эмм... так секретный текст делать будем, не?")
            secret_message = (await conv.get_response()).raw_text
        print(secret_message)

        encoded_message = secret.create_message_with_hidden_part(cover_message, secret_message)
        await conv.send_message('Все, мы скрафтили секретное послание. Отправляй кому следует, и пусть получатель расшифрует его с помощью decode')
        await conv.send_message(encoded_message)


@bot.on(events.NewMessage(pattern='/decode'))
async def do_decode(event):
    async with bot.conversation(event.chat_id) as conv:
        await conv.send_message('Похоже, у тебя есть секретное сообщение, которое надо расшифровать. Давай его сюда')
        cover_message_with_hidden_part = (await conv.get_response()).raw_text
        while not any(x.isalpha() for x in cover_message_with_hidden_part):
            await conv.send_message('Все еще ждем, ага ')
            cover_message_with_hidden_part = (await conv.get_response()).raw_text
        print(cover_message_with_hidden_part)
        decoded_message = secret.get_secret_message(cover_message_with_hidden_part)
        if len(decoded_message) > 0:
            await conv.send_message('Обнаружили в этом сообщении cекретную часть, вот она ниже щас придет:')
            await conv.send_message(decoded_message)            
        else:
            await conv.send_message('Ничего спрятанного тут не нашлось, текст как текст')


def main():
    """Start the bot."""
    bot.run_until_disconnected()


if __name__ == '__main__':
    main()
