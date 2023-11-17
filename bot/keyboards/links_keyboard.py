from typing import Sequence, Optional

from aiogram.types import InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import Row


class LinksCallbackFactory(CallbackData, prefix="link"):
    action: str
    position: Optional[int] = None


def dynamic_links(links_list: Sequence[Row], has_link: bool, position: int = 1) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if has_link:
        builder.button(text="Видалити посилання🗑", callback_data=LinksCallbackFactory(action="remove_link",
                                                                                      position=position))
    else:
        builder.button(text="Додати посилання🔗", callback_data=LinksCallbackFactory(action="add_link",
                                                                                    position=position))

    if position == 1:
        builder.button(text="⛔️", callback_data=LinksCallbackFactory(action="stop"), position=position)
        builder.button(text=f"{position}/{len(links_list)}",
                       callback_data=LinksCallbackFactory(action="length", position=position))
        builder.button(text="▶️", callback_data=LinksCallbackFactory(action="next", position=position+1))

    elif position == len(links_list):
        builder.button(text="◀️", callback_data=LinksCallbackFactory(action="next", position=position-1))
        builder.button(text=f"{position}/{len(links_list)}",
                       callback_data=LinksCallbackFactory(action="length", position=position))
        builder.button(text="⛔️", callback_data=LinksCallbackFactory(action="stop", position=position))

    else:
        builder.button(text="◀️", callback_data=LinksCallbackFactory(action="next", position=position-1))
        builder.button(text=f"{position}/{len(links_list)}",
                       callback_data=LinksCallbackFactory(action="length", position=position))
        builder.button(text="▶️", callback_data=LinksCallbackFactory(action="next", position=position+1))

    builder.adjust(1, 3)

    return builder.as_markup()
