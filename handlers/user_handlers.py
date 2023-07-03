import time
from aiogram import Router, Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from lexic.lexic import LEXICON_RU
from datetime import datetime
from random import choice
from game_logic import cities, log, first_letters, book, rule, podskazka, intel
from bot import main
# from main import bot


# Инициализируем роутер уровня модуля
router: Router = Router()

# mode: str = 'Hard'
# adding: bool = False
# bot_word: str = ''
# player_word: str = ''
# used: list = []

# кнопки как доп опция ответа
button_play: KeyboardButton = KeyboardButton(text='/play')
button_read: KeyboardButton = KeyboardButton(text='/read')
button_help: KeyboardButton = KeyboardButton(text='/help')
button_stop: KeyboardButton = KeyboardButton(text='/stop')
# расклады клавиатур из этих кнопок
keyboard_start: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[button_read, button_play]], resize_keyboard=True)
keyboard_ingame: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[button_help, button_read, button_stop]], resize_keyboard=True)

admins = ["992863889"]

@router.message(Command(commands=['start']))
async def process_start_command(message: Message, bot: Bot):
    m = message.from_user
    user = str(m.id)
    log('logs.json', 'logs', f'{datetime.now().strftime("%d/%m/%Y %H:%M")}, {m.full_name}, @{m.username}, id {user},'
                             f' {m.language_code}')
    log('logs.json', user, '/start')

    # book[user] = {"used": [], "bot_word": '', "player_word": '', mode: 'Hard'}

    await message.answer(text=LEXICON_RU['/start'], reply_markup=keyboard_start)

    # заметно сообщить админу, кто нажал старт
    intel(bot, m, admins, False)


# /play
@router.message(Command(commands=['play']))
async def process_play_command(message: Message, bot: Bot):
    user = str(message.from_user.id)

    # Создание учета текущей игры
    book.setdefault(user, {'used': [], 'bot_word': '', 'player_word': '', 'help_word': 'й', 'mode': 'Hard'})
    print(book)

    #  Генерация первого хода
    r = choice(first_letters)
    print(r)
    book[user]['bot_word'] = choice(cities[r])
    book[user]['used'].append(book[user]['bot_word'])

    await message.answer(f'Я начну: {book[user]["bot_word"]}', reply_markup=keyboard_ingame)
    log('logs.json', user, book[user]["bot_word"].upper())

    # незаметно сообщить админу, кто нажал play
    intel(bot, message, admins, True)


# gamemode
@router.message(Command(commands=['mode']))
async def process_mode_command(message: Message):
    user = str(message.from_user.id)
    log('logs.json', user, '/mode')

    if book.get(user):
        if book[user]['mode'] == 'Hard':
            book[user]['mode'] = 'Easy'
        else:
            book[user]['mode'] = 'Hard'
        await message.answer(f'Режим изменен на {book[user]["mode"]}. Тебе на {rule(book[user]["bot_word"]).upper()}.')
    else:
        await message.answer('Режим можно изменить только во время игры - /play.\n'
                             'При старте режим всегда Hard - так интересней :)')


# конец игры
@router.message(Command(commands=['stop']))
async def process_cancel_command(message: Message):
    user = str(message.from_user.id)
    log('logs.json', user, '/stop')
    if book.get(user):
        end = ''
        for j in book[user]['used']:
            end += (j + ', ')
        await message.answer(f'Конец, мы назвали {len(book[user]["used"])} города(ов): {end[:-2]}.')
        del book[user]
    else:
        await message.answer('Так мы еще не начали, жми /start')
    print(book)

# /help подсказка
@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    user = str(message.from_user.id)
    log('logs.json', user, '/help')

    if book.get(user):
        while book[user]["help_word"] in book[user]["used"] or book[user]["help_word"][0].lower() != rule(
                book[user]["bot_word"]).lower() or len(book[user]["help_word"]) < 3:

            book[user]["help_word"] = choice(cities[rule(book[user]["bot_word"])])
        await message.answer(podskazka(book[user]["help_word"]))
        book[user]["help_word"] = 'й'



    else:
        await message.answer('Так мы еще не начали, жми /play')


# read
@router.message(Command(commands=['read']))
async def process_read_command(message: Message):
    user = str(message.from_user.id)
    log('logs.json', str(user), '/read')

    await message.answer(text=LEXICON_RU['/read'], parse_mode='HTML')

    # если с этим юзером идет игра, напомним на какую ему букву
    if book.get(user):
        time.sleep(1)
        await message.answer(f'Сейчас тебе на {rule(book[user]["bot_word"]).upper()}!')


# /add
@router.message(Command(commands=['add']))
async def add(message: Message):
    log('logs.json', str(message.from_user.id), message.text)
    # await message.answer('Перечисляй города одним сообщением в любом виде')
    await message.answer(LEXICON_RU['/add'])

    # await message.answer('Вводи города одним сообщением через пробел, чтобы добавить их в мою базу')
    # async with asyncio.wait_for(message.text, timeout=) as new_message:
    #     adds = str(message.text).split()
    #     with open("add.txt", "a", encoding='utf-8') as w:
    #         w.write(*adds)
    #         w.write('\n\n')
    #     await message.answer(f'Внесено городов на рассмотрение моим хозяином: {len(adds)}.')

# # добавление городов после команды /add
# @router.message()
# async def add(message: Message):
#     log(str(message.from_user.id), message.text)
#
#     # await message.answer('Функция пока не работает :(')
#     await message.answer('Перечисляй города в любом виде')


# если ввод не на доступную букву
@router.message(lambda x: x.text and rule(str(x.text).lower()) not in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
async def process_text_answer(message: Message):
    user = str(message.from_user.id)

    with open("add.txt", "a", encoding='utf-8') as w:
        w.write(f'{str(message.text)} ')
    await message.answer(f'Я могу только по-русски, тебе на {rule(book[user]["bot_word"]).upper()}')
    print(str(message.text).lower()[-1])


# остальные любые сообщения
@router.message()
async def process_other_text_answers(message: Message):
    user = str(message.from_user.id)

    book[user]["player_word"] = str(message.text).capitalize()

    # проверка первой буквы из хода юзера
    if book[user]["player_word"][0].lower() == rule(book[user]["bot_word"]).lower():

        # проверка уникальности хода
        if book[user]["player_word"].capitalize() in book[user]["used"]:
            await message.answer('Этот город уже был!', reply_markup=keyboard_ingame)

        # Проверка на знание ботом города из хода юзера
        elif book[user]['mode'] == 'Easy' or book[user]["player_word"].capitalize() in cities[
            book[user]["player_word"].lower()[0]]:
            book[user]["used"].append(book[user]["player_word"].capitalize())

            log('logs.json', user, f'{book[user]["player_word"].capitalize()} ')


            # ответ бота
            while book[user]["bot_word"] in book[user]["used"] or book[user]["bot_word"][0].lower() != rule(
                    book[user]["player_word"]).lower():
                book[user]["bot_word"] = choice(cities[rule(book[user]["player_word"])])
            await message.answer(book[user]["bot_word"])

            log('logs.json', user, f'{book[user]["bot_word"].upper()} ')

            book[user]["player_word"] = ''
            book[user]["used"].append(book[user]["bot_word"])

        else:
            await message.answer(f'Не знаю такого, попробуй еще - тебе на {rule(book[user]["bot_word"]).upper()}', reply_markup=keyboard_ingame)
    else:
        await message.answer(f'Первая буква не подходит, тебе на {rule(book[user]["bot_word"]).upper()}', reply_markup=keyboard_ingame)
    print(user, book[user]["used"])