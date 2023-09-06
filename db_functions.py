import sqlite3
import datetime

from random import randint

from config import db_name


def get_user(user):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    req_params = (user.chat_id,)
    cur.execute("""SELECT *
                    FROM users
                    WHERE chat_id = ?""", req_params)
    return cur.fetchone()


def save_user(user):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    if not user.stored:
        try:

            req_params = (user.chat_id, user.phone_number, user.last_question,
                          user.start_hour, user.start_minute, user.start_text,
                          user.end_hour, user.end_minute, user.end_text,
                          user.randomize)

            cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", req_params)
            conn.commit()

            user.stored = True
            user.saved = True
        except Exception as exc:
            print(exc)
            user.stored = False
            user.saved = False

    else:
        try:

            req_params = (user.chat_id, user.phone_number, user.last_question,
                          user.start_hour, user.start_minute, user.start_text,
                          user.end_hour, user.end_minute, user.end_text,
                          user.randomize, user.chat_id)

            cur.execute("""UPDATE users 
                    SET 
                    chat_id = ?, 
                    phone_number = ?,
                    last_question = ?,
                    start_hour = ?,
                    start_minute = ?,
                    start_text = ?,
                    end_hour = ?,
                    end_minute = ?,
                    end_text = ?,
                    randomize = ?
                    WHERE chat_id = ?;""", req_params)

            conn.commit()

            user.saved = True
        except Exception as exc:
            print(exc)
            user.saved = False


def create_tables():
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS users(
                chat_id TEXT PRIMARY KEY,
                phone_number TEXT,
                last_question TEXT,
                start_hour INT,
                start_minute INT,
                start_text TEXT,
                end_hour INT,
                end_minute INT,
                end_text TEXT,
                randomize BOOL);
        """)
    conn.commit()


def set_queue(message_queue):
    send_hour = datetime.datetime.now().hour
    send_minute = datetime.datetime.now().minute

    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    req_params = (send_hour, send_minute)
    cur.execute("""SELECT 
                    chat_id,
                    randomize
                    FROM users
                    WHERE start_hour = ? 
                    AND
                    start_minute = ?""", req_params)

    start_users = cur.fetchall()

    for user in start_users:
        use_minute = send_minute
        if user[1]:
            use_minute = send_minute + randint(0, 9)
            if use_minute > 59:
                use_minute = 59

        message_queue[str(user[0])] = {
            'chat_id': int(user[0]),
            'hour': send_hour,
            'minute': use_minute,
            'type': 'start'
        }

    cur.execute("""SELECT 
                    chat_id,
                    randomize
                    FROM users
                    WHERE end_hour = ? 
                    AND
                    end_minute = ?""", req_params)

    end_users = cur.fetchall()

    for user in end_users:
        use_minute = send_minute
        if user[1]:
            use_minute = send_minute + randint(0, 9)
            if use_minute > 59:
                use_minute = 59

        message_queue[str(user[0])] = {
            'chat_id': int(user[0]),
            'hour': send_hour,
            'minute': use_minute,
            'type': 'end'
        }
