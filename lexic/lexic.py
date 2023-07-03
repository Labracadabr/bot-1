from game_logic import dlina

LEXICON_RU: dict[str, str] = {

    '/start': 'Привет!\nДавай сыграем в города.\n'
              f'Я знаю городов: {dlina}.\n\nМожешь нажать:\n'
              f'/read для инструкции, как мной пользоваться\n'
              f'/play для новой игры\n',

    '/read': '<b>Общие правила:</b>\nОтправь мне город, начинающийся на последнюю букву моего города.'
             '\nЕсли мой город оканчивается на Ь или Ъ - то бери следующую с конца букву, например:'
             '\nЕсли я пишу "Казань" - ты можешь написать "Найроби".'
             '\nНа букву Ы, если что, тоже играем - я знаю 26 городов на эту букву.'
             # '\nНасчет буквы ё - тебе нужно писать не "Орел", а "Орёл"\n'
             '\n\n<b>Команды:</b>'
             '\n/start - перезапуск бота'
             '\n/read - почитать инструкцию'
             '\n/play - новая игра'
             '\n/help - подскажу тебе город на нужную букву, но скрою несколько случайных букв, например: Нов**иб*рск'
             '\n/stop - завершить игру и просмотреть итог'
             '\n/add  - предложить дополнительные города'
             '\n/mode - сменить режим игры. Есть два режима:'
             '\n<i>Hard</i> - я принимаю от тебя только те города, которые сам знаю;'
             '\n<i>Easy</i> - я не проверяю, знаю ли город из твоего ответа.\n',

    # '/mode': f'Режим изменен на {book[user][mode]}. Тебе на {rule(book[user]["bot_word"]).upper()}.',

    '/help': '',

    '/add': 'Создателю лень доделать эту функцию :(',

    '/stop': '',

    '1': 'Данный тип апдейтов не поддерживается '
         'методом send_copy',

    '2': 'Данный тип апдейтов не поддерживается '
         'методом send_copy',

    '3': 'Данный тип апдейтов не поддерживается '
         'методом send_copy'

}
