import json
import random

# Игровые данные, правила и переменные
with open("cities_rus.json", "r", encoding='utf-8') as f:
    cities = json.load(f)

# Допустимые первые буквы. Тут все кроме Ъ Ь
first_letters = [
    'а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц',
    'ч', 'ш', 'ы', 'э', 'ю', 'я']

# сколько знаем городов
dlina = 0
for i in cities:
    dlina += len(cities.get(i))

book: dict = {}


# возвращает букву, на которую должно быть след слово
def rule(w):
    w = str(w)
    for k in range(len(w)):
        if w[-k - 1] in first_letters:
            return w[-k - 1]


# Запись данных item в указанный json file по ключу key
def log(file, key, item):
    with open(file, encoding='utf-8') as f:
        data = json.load(f)

    data.setdefault(key, []).append(item)

    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
# не рабочий варик
# def log(file, key, item):
#     with open(file, encoding='utf-8') as f1, open(file, 'w', encoding='utf-8') as f2:
#         data = json.load(f1)
#         data.setdefault(key, []).append(item)
#         json.dump(data, f2, indent=2, ensure_ascii=False)


#  Новосибирск >random> Нов**иб*рск
def podskazka(word):
    l = len(word)
    if l < 7:
        stars = 1
    elif l == 8:
        stars = 2
    elif l > 13:
        stars = 4
    else:
        stars = 3

    hidden_letters = "*" * (len(word) - 2)  # скрытые символы *

    # выбираем случайные позиции для скрытия букв
    indices = random.sample(range(1, len(word) - 1), stars)

    # формируем измененное слово
    new_word = ""
    for i in range(len(word)):
        if i in indices:
            new_word += hidden_letters[i-1]
        else:
            new_word += word[i]

    return new_word


#  Палит админу действия юзеров. Первые три аргумента вписать такими, как есть тут
def intel(bot, message, admins, silence: bool):
    user = str(message.from_user.id)
    if user not in admins:
        for i in admins:
            await bot.send_message(text=f'#{message.text} id{user} {message.from_user.full_name}'
                                        f' @{message.from_user.username}', chat_id=i, disable_notification=silence)



