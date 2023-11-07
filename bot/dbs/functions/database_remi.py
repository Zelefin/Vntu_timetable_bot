import sqlite3

global connect
global cursor
connect = sqlite3.connect('users_reminder.db', check_same_thread=False)
cursor = connect.cursor()


def when_start_min(n):  # ! UTC TIME
    all_starts = ["05:10", "06:10", "07:10", "08:10", "09:10",
                  "10:10", "11:10", "12:05", "13:00"]
    start = all_starts[n - 1]
    return start


def when_start_now(n):  # ! UTC TIME
    all_starts = ["05:15", "06:15", "07:15", "08:15", "09:15",
                  "10:15", "11:15", "12:10", "13:05"]
    start = all_starts[n - 1]
    return start


timetable_times = ["04:00", "04:30", "05:00", "06:00"]


def should_send_noti(time):
    cursor.execute(
        "SELECT id FROM login_id WHERE time = ?", (time,))
    rows = cursor.fetchall()

    if rows:
        # Если есть совпадения, то получаем список login_id
        login_ids = [row[0] for row in rows]

        # Удаляем записи из базы данных
        for login in login_ids:
            cursor.execute(
                "UPDATE login_id SET time = NULL WHERE id = ?", (login,))
        connect.commit()

        # Возвращаем список login_id, которые нужно отправить
        return ["Yes", login_ids]

    # Если совпадений нет, возвращаем пустой список
    return ["No"]


def should_send_timetable(time):
    cursor.execute(
        "SELECT id FROM login_id WHERE sub = ?", (time,))
    rows = cursor.fetchall()

    if rows:
        # Если есть совпадения, то получаем список login_id
        login_ids = [row[0] for row in rows]

        # Возвращаем список login_id, которые нужно отправить
        return ["Yes", login_ids]

    # Если совпадений нет, возвращаем пустой список
    return ["No"]


def add_user_total(uid):
    cursor.execute("SELECT id FROM login_id WHERE id = %s" % (uid,))
    data = cursor.fetchone()

    if (data is None):
        cursor.execute("INSERT INTO login_id VALUES(?, NULL, NULL)",
                       (uid,))
        connect.commit()


def timetable_send(uid, time):
    cursor.execute(
        "SELECT id FROM login_id WHERE id = %s AND sub IS NOT NULL" % (uid,))
    data = cursor.fetchone()

    if data is None:
        cursor.execute(
            "UPDATE login_id SET sub = ? WHERE id = ?", (timetable_times[int(time)], uid))
        connect.commit()
        return 00
    else:
        return 11


def timetable_stop(uid):
    cursor.execute("UPDATE login_id SET sub = NULL WHERE id = ?", (uid,))
    connect.commit()


def check_table(uid):
    cursor.execute(
        "SELECT id FROM login_id WHERE id = %s AND sub IS NOT NULL" % (uid,))
    data = cursor.fetchone()

    if (data is None):
        return "NotGetter"
    else:
        return "Getter"


def check_remi(uid):
    cursor.execute(
        "SELECT id FROM login_id WHERE id = %s AND time IS NOT NULL" % (uid,))
    data = cursor.fetchone()

    if (data is None):
        return "Valid"
    else:
        return "NotVal"


def add_user_remi_min(uid, lesson):

    # check id in fields

    cursor.execute(
        "SELECT id FROM login_id WHERE id = %s AND time IS NOT NULL" % (uid,))
    data = cursor.fetchone()

    if (data is None):
        # add values in fields
        time = when_start_min(int(lesson))
        cursor.execute(
            "UPDATE login_id SET time = ? WHERE id = ?", (time, uid))
        connect.commit()
        return 00

    else:
        return 11


def add_user_remi_now(uid, lesson):

    # check id in fields
    cursor.execute(
        "SELECT id FROM login_id WHERE id = %s AND time IS NOT NULL" % (uid,))
    data = cursor.fetchone()

    if (data is None):
        # add values in fields
        time = when_start_now(int(lesson))
        cursor.execute(
            "UPDATE login_id SET time = ? WHERE id = ?;", (time, uid))

        connect.commit()
        return 00

    else:
        return 11


def remove_noti_polite(uid):
    cursor.execute("UPDATE login_id SET time = NULL WHERE id = ?;", (uid,))
    connect.commit()


def remove_noti(uid):
    cursor.execute("DELETE FROM login_id WHERE id = %s" % (uid,))
    connect.commit()
