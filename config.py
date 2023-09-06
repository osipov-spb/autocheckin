telegram_access_token = ''
test = 123
telegram_url = 'https://web.telegram.org'

chat_main_url = 'https://web.telegram.org/a/#'
chat_id = '132005438'


db_name = 'app_data.db'

bot_texts = {
    'phone_number': 'Для продолжения необходимо указать некоторые данные\n---\nВведите свой телефон для '
                    'авторизации в telegram в формате +79999999999',
    'start_hour': 'Введите час, когда будем чекиниться на приход.\nДопустивые значения 0 - 23'
                  '\nЧасовой пояс UTC+3 (Москва)',
    'start_minute': 'Введите минуту, когда будем чекиниться на приход.\nДопустивые значения 0 - 59',
    'start_text': 'Укажите текст для отметки при чекине на приход',
    'end_hour': 'Введите час, когда будем чекиниться на уход.\nДопустивые значения 0 - 23'
                  '\nЧасовой пояс UTC+3 (Москва)',
    'end_minute': 'Введите минуту, когда будем чекиниться на уход.\nДопустивые значения 0 - 59',
    'end_text': 'Укажите текст для отметки при чекине на уход',
    'randomize': 'Рандомизировать время отметки в интервале до 10 минут?\nНапишите Да или Нет',
    'auth': 'Данные успешно сохранены.\nТеперь необходимо пройти авторизацию в telegram от вашего имени',
    'auth_attempt_success': 'Введите полученный код В ОБРАТНОМ ПОРЯДКЕ пример: 123456 -> 654321',
    'auth_attempt_failed': 'Ошибка при попытке авторизоваться.\nОтправьте номер телефона еще раз в формате +79999999999',
    'auth_success': 'Авторизация прошла успешно',
    'auth_failed': 'Не удалось пройти авторизацию.\nСейчас вам придет новый код.\nОтправьте его в ответном сообщении В ОБРАТНОМ ПОРЯДКЕ пример: 123456 -> 654321',
    'auth_ask': 'Требуется повторная авторизация.\nПожалуйста, выберите пункт "Авторизация" в  списке комманд бота или напишите /auth',
    'auth_asked_start': 'Начинаем авторизацию в telegram от вашего имени',
    'checkin_success': 'Отметка на приход успешна',
    'checkin_failed': 'Не удалось отметиться на приход',
    'checkout_success': 'Отметка на уход успешна',
    'checkout_failed': 'Не удалось отметиться на уход',
    'unknown_command': 'Не понял вас, возможно вы ввели некорректные данные. Попробуйте еще раз'
}


class Keys:
    """
    Set of special keys codes.
    """

    NULL = '\ue000'
    CANCEL = '\ue001'  # ^break
    HELP = '\ue002'
    BACKSPACE = '\ue003'
    BACK_SPACE = BACKSPACE
    TAB = '\ue004'
    CLEAR = '\ue005'
    RETURN = '\ue006'
    ENTER = '\ue007'
    SHIFT = '\ue008'
    LEFT_SHIFT = SHIFT
    CONTROL = '\ue009'
    LEFT_CONTROL = CONTROL
    ALT = '\ue00a'
    LEFT_ALT = ALT
    PAUSE = '\ue00b'
    ESCAPE = '\ue00c'
    SPACE = '\ue00d'
    PAGE_UP = '\ue00e'
    PAGE_DOWN = '\ue00f'
    END = '\ue010'
    HOME = '\ue011'
    LEFT = '\ue012'
    ARROW_LEFT = LEFT
    UP = '\ue013'
    ARROW_UP = UP
    RIGHT = '\ue014'
    ARROW_RIGHT = RIGHT
    DOWN = '\ue015'
    ARROW_DOWN = DOWN
    INSERT = '\ue016'
    DELETE = '\ue017'
    SEMICOLON = '\ue018'
    EQUALS = '\ue019'

    NUMPAD0 = '\ue01a'  # number pad keys
    NUMPAD1 = '\ue01b'
    NUMPAD2 = '\ue01c'
    NUMPAD3 = '\ue01d'
    NUMPAD4 = '\ue01e'
    NUMPAD5 = '\ue01f'
    NUMPAD6 = '\ue020'
    NUMPAD7 = '\ue021'
    NUMPAD8 = '\ue022'
    NUMPAD9 = '\ue023'
    MULTIPLY = '\ue024'
    ADD = '\ue025'
    SEPARATOR = '\ue026'
    SUBTRACT = '\ue027'
    DECIMAL = '\ue028'
    DIVIDE = '\ue029'

    F1 = '\ue031'  # function  keys
    F2 = '\ue032'
    F3 = '\ue033'
    F4 = '\ue034'
    F5 = '\ue035'
    F6 = '\ue036'
    F7 = '\ue037'
    F8 = '\ue038'
    F9 = '\ue039'
    F10 = '\ue03a'
    F11 = '\ue03b'
    F12 = '\ue03c'

    META = '\ue03d'
    COMMAND = '\ue03d'
    ZENKAKU_HANKAKU = '\ue040'