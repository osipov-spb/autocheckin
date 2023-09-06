import datetime
from threading import Thread
from time import sleep

import telebot

from config import telegram_access_token, bot_texts
from User import User
from db_functions import set_queue


bot = telebot.TeleBot(telegram_access_token)

users = {}
message_queue = {}


def start_bot():
    t = Thread(target=bot_daemon)
    t2 = Thread(target=sender_daemon)
    t3 = Thread(target=queue_daemon)
    t.start()
    t2.start()
    t3.start()


def queue_daemon():
    global message_queue
    while True:
        try:
            set_queue(message_queue)
            sleep(30)
        except Exception as exc:
            pass


def sender_daemon():
    global message_queue
    global users
    while True:
        try:
            current_hour = datetime.datetime.now().hour
            current_minute = datetime.datetime.now().minute

            safe_queue = message_queue;

            for queue_elem in safe_queue:
                if (message_queue[queue_elem]['hour'] == current_hour \
                        and message_queue[queue_elem]['minute'] < current_minute) or \
                        message_queue[queue_elem]['hour'] < current_hour:
                    if queue_elem in users and users[queue_elem].auth_complete:
                        user = users[queue_elem]
                        success = user.check_in()
                        if success:
                            del message_queue[queue_elem]
                    else:
                        if queue_elem not in users:
                            users[queue_elem] = User(message_queue[queue_elem]['chat_id'])
                            user = users[queue_elem]
                        else:
                            user = users[queue_elem]

                        user.get()
                        if user.last_question != 'auth' and user.last_question != 'auth_attempt_success':
                            bot.send_message(queue_elem, bot_texts['auth_ask'],
                                             disable_notification=False)
                            user.last_question = 'auth'
                            user.save()
            sleep(10)
        except Exception as exc:
            sleep(10)
            pass


def bot_daemon():
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as exc:
            pass


@bot.message_handler(content_types=['text'])
def message_handler(message):
    global users

    if str(message.chat.id) in users.keys():
        user = users[str(message.chat.id)]
    else:
        users[str(message.chat.id)] = User(message.chat.id)
        user = users[str(message.chat.id)]

    if message.text == '/start':
        bot.send_message(message.chat.id, bot_texts['phone_number'],
                         disable_notification=False)

        user.last_question = 'phone_number'
        user.save()
    elif message.text == '/auth':
        try:
            bot.send_message(message.chat.id, bot_texts['auth_asked_start'],
                             disable_notification=False)

            auth_success = user.auth()

            if auth_success:
                bot.send_message(message.chat.id, bot_texts['auth_attempt_success'],
                                 disable_notification=False)
                user.last_question = 'auth_attempt_success'
                user.save()
            else:
                bot.send_message(message.chat.id, bot_texts['auth_attempt_failed'],
                                 disable_notification=False)
                user.last_question = 'auth_attempt_failed'
                user.save()

        except:
            bot.send_message(message.chat.id, bot_texts['unknown_command'],
                             disable_notification=False)

            bot.send_message(message.chat.id, bot_texts['auth_attempt_failed'],
                             disable_notification=False)
    else:
        if user.last_question == 'phone_number':
            try:
                user.phone_number = message.text
                user.last_question = 'start_hour'
                user.save()

                bot.send_message(message.chat.id, bot_texts['start_hour'],
                                 disable_notification=False)

            except:
                bot.send_message(message.chat.id, bot_texts['unknown_command'],
                                 disable_notification=False)

                bot.send_message(message.chat.id, bot_texts['phone_number'],
                                 disable_notification=False)

        elif user.last_question == 'start_hour':
            try:
                user.start_hour = int(message.text)
                user.last_question = 'start_minute'
                user.save()

                bot.send_message(message.chat.id, bot_texts['start_minute'],
                                 disable_notification=False)

            except:
                bot.send_message(message.chat.id, bot_texts['unknown_command'],
                                 disable_notification=False)

                bot.send_message(message.chat.id, bot_texts['start_hour'],
                                 disable_notification=False)
        elif user.last_question == 'start_minute':
            try:
                user.start_minute = int(message.text)
                user.last_question = 'start_text'
                user.save()

                bot.send_message(message.chat.id, bot_texts['start_text'],
                                 disable_notification=False)

            except:
                bot.send_message(message.chat.id, bot_texts['unknown_command'],
                                 disable_notification=False)

                bot.send_message(message.chat.id, bot_texts['start_minute'],
                                 disable_notification=False)
        elif user.last_question == 'start_text':
            try:
                user.start_text = message.text
                user.last_question = 'end_hour'
                user.save()

                bot.send_message(message.chat.id, bot_texts['end_hour'],
                                 disable_notification=False)

            except:
                bot.send_message(message.chat.id, bot_texts['unknown_command'],
                                 disable_notification=False)

                bot.send_message(message.chat.id, bot_texts['start_text'],
                                 disable_notification=False)
        elif user.last_question == 'end_hour':
            try:
                user.end_hour = int(message.text)
                user.last_question = 'end_minute'
                user.save()

                bot.send_message(message.chat.id, bot_texts['end_minute'],
                                 disable_notification=False)

            except:
                bot.send_message(message.chat.id, bot_texts['unknown_command'],
                                 disable_notification=False)

                bot.send_message(message.chat.id, bot_texts['end_hour'],
                                 disable_notification=False)
        elif user.last_question == 'end_minute':
            try:
                user.end_minute = int(message.text)
                user.last_question = 'end_text'
                user.save()

                bot.send_message(message.chat.id, bot_texts['end_text'],
                                 disable_notification=False)

            except:
                bot.send_message(message.chat.id, bot_texts['unknown_command'],
                                 disable_notification=False)

                bot.send_message(message.chat.id, bot_texts['end_minute'],
                                 disable_notification=False)
        elif user.last_question == 'end_text':
            try:
                user.end_text = message.text
                user.last_question = 'randomize'
                user.save()

                bot.send_message(message.chat.id, bot_texts['randomize'],
                                 disable_notification=False)

            except:
                bot.send_message(message.chat.id, bot_texts['unknown_command'],
                                 disable_notification=False)

                bot.send_message(message.chat.id, bot_texts['end_text'],
                                 disable_notification=False)
        elif user.last_question == 'randomize':
            try:
                if message.text == 'Да' or message.text == 'да' or message.text == 'ДА':
                    user.randomize = True
                elif message.text == 'Нет' or message.text == 'нет' or message.text == 'НЕТ':
                    user.randomize = False
                else:
                    raise

                user.last_question = 'auth'
                user.save()
                bot.send_message(message.chat.id, bot_texts['auth'],
                                 disable_notification=False)

                auth_success = user.auth()

                if auth_success:
                    bot.send_message(message.chat.id, bot_texts['auth_attempt_success'],
                                     disable_notification=False)
                    user.last_question = 'auth_attempt_success'
                    user.save()
                else:
                    bot.send_message(message.chat.id, bot_texts['auth_attempt_failed'],
                                     disable_notification=False)
                    user.last_question = 'auth_attempt_failed'
                    user.save()

            except:
                bot.send_message(message.chat.id, bot_texts['unknown_command'],
                                 disable_notification=False)

                bot.send_message(message.chat.id, bot_texts['randomize'],
                                 disable_notification=False)
        elif user.last_question == 'auth':
            try:
                auth_success = user.auth()

                if auth_success:
                    bot.send_message(message.chat.id, bot_texts['auth_attempt_success'],
                                     disable_notification=False)
                    user.last_question = 'auth_attempt_success'
                    user.save()
                else:
                    bot.send_message(message.chat.id, bot_texts['auth_attempt_failed'],
                                     disable_notification=False)
                    user.last_question = 'auth_attempt_failed'
                    user.save()

            except:
                bot.send_message(message.chat.id, bot_texts['unknown_command'],
                                 disable_notification=False)

                bot.send_message(message.chat.id, bot_texts['auth_attempt_failed'],
                                 disable_notification=False)
        elif user.last_question == 'auth_attempt_success':
            try:
                auth_success = user.auth(message.text)
                if auth_success:
                    bot.send_message(message.chat.id, bot_texts['auth_success'],
                                     disable_notification=False)
                    user.last_question = 'auth_success'
                    user.save()
                else:
                    bot.send_message(message.chat.id, bot_texts['auth_attempt_failed'],
                                     disable_notification=False)
                    user.last_question = 'auth_attempt_failed'
                    user.save()
            except:
                bot.send_message(message.chat.id, bot_texts['unknown_command'],
                                 disable_notification=False)

                bot.send_message(message.chat.id, bot_texts['auth_attempt_failed'],
                                 disable_notification=False)

        elif user.last_question == 'auth_attempt_failed':
            try:
                user.phone_number = message.text
                user.last_question = 'randomize'
                user.save()

                auth_success = user.auth()

                if auth_success:
                    bot.send_message(message.chat.id, bot_texts['auth_attempt_success'],
                                     disable_notification=False)
                    user.last_question = 'auth_attempt_success'
                    user.save()
                else:
                    bot.send_message(message.chat.id, bot_texts['auth_attempt_failed'],
                                     disable_notification=False)
                    user.last_question = 'auth_attempt_failed'
                    user.save()
            except:
                bot.send_message(message.chat.id, bot_texts['unknown_command'],
                                 disable_notification=False)

                bot.send_message(message.chat.id, bot_texts['phone_number'],
                                 disable_notification=False)

