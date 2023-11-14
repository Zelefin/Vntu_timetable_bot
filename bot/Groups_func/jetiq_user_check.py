import logging
import aiohttp


async def jetiq_check(message_text: str) -> bool:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://my.vntu.edu.ua/api/user-query.do?search={message_text}") as response:
                r = await response.json()

                if r['content'][0]['name'] == message_text:
                    return True
                else:
                    return False

    except Exception as e:
        logging.info(f"JETIQ CHECK GOT EXCEPTION # {e}")
        return False
