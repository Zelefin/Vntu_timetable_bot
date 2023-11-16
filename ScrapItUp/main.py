from ScrapItUp.html_scraper import generate_html
from ScrapItUp.scrap_to_json import scrap_html_to_json
from ScrapItUp.message_constructor import weeks_constructor


async def scrapitup_main() -> None:
    await generate_html()
    scrap_html_to_json()
    weeks_constructor()
