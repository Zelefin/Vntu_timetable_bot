from datetime import date, datetime


def cur_week() -> int:

    if (datetime.today().weekday() == 5) or (datetime.today().weekday() == 6):

        if ((date.isocalendar(date.today())[1]) % 2) == 0:
            # парний
            w_cur = 2
        else:
            # непарний
            w_cur = 1
    else:
        if ((date.isocalendar(date.today())[1]-1) % 2) == 0:
            # парний
            w_cur = 2
        else:
            # непарний
            w_cur = 1
    return w_cur


def cur_day():

    day = datetime.today().weekday() + 1

    if day >= 6:
        day = 1

    return day
