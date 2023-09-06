from db_functions import get_user, save_user
from selenium_functions import get_driver, auth_user, check_user


class User:
    # db data
    chat_id: int = 0
    phone_number: str = ''
    last_question: str = ''
    start_hour: int = 11
    start_minute: int = 0
    start_text: str = 'Начал'
    end_hour: int = 20
    end_minute: int = 0
    end_text: str = 'Закончил'
    randomize: bool = True

    # status
    stored: bool = False
    saved: bool = False
    auth_passed: bool = False
    auth_complete: bool = False

    # other
    driver = None

    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.saved = False

        self.get()

        if self.driver is None:
            self.driver = get_driver()

    def get(self):
        result = get_user(self)
        if result is None:
            self.stored = False

            self.save()
        else:
            self.chat_id = result[0]
            self.phone_number = result[1]
            self.last_question = result[2]
            self.start_hour = result[3]
            self.start_minute = result[4]
            self.start_text = result[5]
            self.end_hour = result[6]
            self.end_minute = result[7]
            self.end_text = result[8]
            self.randomize = result[9]

            self.saved = True
            self.stored = True

    def save(self):
        self.saved = False
        save_user(self)

    def auth(self, pass_code=''):

        if self.driver is None:
            self.driver = get_driver()

        return auth_user(self, pass_code)

    def check_in(self):
        return check_user(self, 'in')

    def check_out(self):
        return check_user(self, 'out')
