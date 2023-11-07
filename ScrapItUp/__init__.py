__all__ = ["generate_html", "scrap_html_to_json", "weeks_constructor", "scrapitup_main", "groups_ids"]

from .html_scraper import generate_html
from .scrap_to_json import scrap_html_to_json
from .message_constructor import weeks_constructor
from .main import scrapitup_main
from .ids_dict import groups_ids
