import logging
import aiohttp
from yarl import URL

user_agent = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/86.0.4240.198 Safari/537.36 OPR/72.0.3815.465 (Edition Yx GX)',
}

cookies = {
    "VNTU_CSRFToken": "",
    "VNTU_UAToken": ""
}


async def jetiq_check(message_text: str) -> bool | str:
    try:
        async with aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar()) as session:
            async with session.get(f"https://my.vntu.edu.ua/api/user-query.do?search={message_text}",
                                   headers=user_agent, cookies=cookies) as response:
                r: dict = await response.json()

                if r.get('error'):
                    await get_new_cookies()
                    new_check = await jetiq_check(message_text)
                    if isinstance(new_check, str):
                        return str(r)
                    else:
                        return new_check

                if r.get('content'):
                    if r['content'][0]['name'] == message_text:
                        return True
                    else:
                        return False
                else:
                    return False

    except Exception as e:
        logging.info(f"JETIQ CHECK GOT EXCEPTION # {e}")
        return str(e)


async def get_new_cookies():
    async with aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar()) as session:
        async with session.get("https://my.vntu.edu.ua/user/signin/",
                               headers=user_agent):

            new_cookies = session.cookie_jar.filter_cookies(request_url=URL("https://my.vntu.edu.ua"))

            cookies['VNTU_CSRFToken'] = str(new_cookies['VNTU_CSRFToken'])
            cookies['VNTU_UAToken'] = str(new_cookies['VNTU_UAToken'])
