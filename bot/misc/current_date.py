import datetime


def current_week() -> str:
    return (
        "firstWeek"
        if datetime.date.isocalendar(datetime.date.today())[1] % 2 == 0
        else "secondWeek"
    )


def current_day() -> int:
    return datetime.date.today().weekday()
