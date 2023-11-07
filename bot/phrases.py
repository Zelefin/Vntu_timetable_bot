
bot_commands = [
    ('start', 'Це команда старт!'),
    ('design', 'Це команда дизайн'),
    ('registration', 'Це команда реєстрації'),
    ('delete_me', 'Це команда видалення'),
    ('feedback', 'Це команда фідбеку')
]

admin_id = 845597372
groups = ["1ПІ-23б", "2ПІ-23б", "3ПІ-23б", "4ПІ-23б", "5ПІ-23б", "6ПІ-23б"]
subgroups = ["1 Підгрупа", "2 Підгрупа"]
days = ["Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця"]


start_phrases = {
    "choosing_not_reg": "Привіт, <b>{n}</b>!\nОберіть свою группу зі списку:",
    "choosing_reg": "Виберіть день:",
    "choose_subgroup": "Тепер виберіть підгрупу:",
    "wrong_group": "Я не знаю такої групи.\n\nБудь ласка, виберіть групу з цього списку:",
    "choose_day": "Тепер виберіть день:",
    "wrong_subgroup": "Я не знаю такої підгрупи.\n\nБудь ласка, виберіть підгрупу з цього списку:",
    "wrong_day": "Я не знаю такого дня.\n\nБудь ласка, виберіть день з цього списку:"
}

start_midlwr_phrases = {
    "first_visit": "Це твій перший запуск бота!"
}

design_phrases = {
    "just_it": "Достатньо обрати день тижня!"
}
design_midlwr_phrases = {
    "message_ans": "Ця функція доступна лише зареєстрованим користувачам!",
    "callback_ans": "Ця функція доступна лише зареєстрованим користувачам!"
}


reg_phrases = {

    "choose_group": "Реєcтруємось!\nОберіть свою группу зі списку:",
    "choose_subgroup": "Тепер виберіть свою підгрупу:",
    "incorrect_group": "Я не знаю такої групи.\n\nБудь ласка, виберіть підгрупу з цього списку:",
    "incorrect_subgroup": "Я не знаю такої підгрупи.\n\nБудь ласка, виберіть підгрупу з цього списку:",
    "sucsessful": "Вас зареєстровано!\nВаша група: <b>{g}</b>\nВаша підгрупа: <b>{s} Підгрупа</b>",
    "failed": "Упс... Щось пішло не так..."
}
reg_mdlwr_phrases = {
    "message_ans": "Ви вже зареєстровані!"
}

del_phrases = {
    "sucsessful": "Вас видалено з бази!",
    "unsucsessful": "Виникла помилка! Вас не видалено з бази!"
}

feedback_phrases = {
    "on_send": "Очікую повідомлення довжиною не більше 250 символів...\nЩоб нічого не відправляти напишіть /cancel",
    "sending_stop": "Нічого не відправляю...",
    "too_long": "Повідомлення занадто довге, не відправляю",
    "good": "Чудово, повідомлення відправлено!",
    "bad_stuff": "Виникла помилка. Будь ласка відправляйте лише текст!"
}
