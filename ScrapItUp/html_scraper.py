import logging
import os
from pathlib import Path

from dotenv import load_dotenv


import aiohttp
from bs4 import BeautifulSoup

from ScrapItUp.ids_dict import groups_ids


PATH = Path.cwd()

if PATH.name == "bot":
    PATH = PATH.parent


async def generate_html():
    load_dotenv(f"{PATH}/bot/.env")

    async with aiohttp.ClientSession() as session:

        login_url = 'https://my.vntu.edu.ua/user/signin/'  # Ссылка для входа

        response = await session.get(login_url)

        response_text = await response.text()

        soup = BeautifulSoup(response_text, 'html.parser')
        csrf_token = soup.find('input', {'name': 'csrf_token'})['value']
        # Херня нужна чтобы получить рабочий csrf_token

        header = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0'
        }

        data = {
            'csrf_token': csrf_token,
            'user_field': os.getenv("JETIQ_LOGIN"),
            'avatar_id': os.getenv("JETIQ_AVATAR_ID"),
            'autologin': 'false',
            'pwd_field': os.getenv("JETIQ_PASSWORD")
        }  # Не работает без autologin и avatar_id

        await session.post(login_url, data=data, headers=header)
        # заходим на аккаунт

        # Ссылка для входа в main акк
        protected_url = 'https://my.vntu.edu.ua/user/go/jetiq.cgi'

        r = await session.get(protected_url, headers=header)
        r_text = await r.text()
        soup = BeautifulSoup(r_text, 'html.parser')
        uuid = soup.find('input', {'name': 'uuid'})['value']
        uatoken = soup.find('input', {'name': 'uatoken'})['value']
        # Херня чтобы получить uuid и uatoken которые нужны для активации(?) phpsessid

        next_data = {
            'uuid': uuid,
            'uatoken': uatoken
        }

        # user_switch куда идут все эти токены и айди
        next_url = 'https://iq.vntu.edu.ua/entry/user_switch.php'
        await session.post(next_url, headers=header, data=next_data)
        # print(result.cookies) # тут можна по приколу будет кукисы подменять, но пока не хочу

        # ????
        # * PROFIT!!

        for key, group_id in groups_ids.items():
            response2 = await session.post(
                f'https://iq.vntu.edu.ua/b04213/curriculum/c_list.php?view=g&group_id={group_id}', headers=header)

            with open(f'{PATH}/ScrapItUp/Groups_html/{group_id}.html', 'w') as f:
                response2_text = await response2.text()
                logging.info("I GOT THIS!")
                f.write(response2_text)
