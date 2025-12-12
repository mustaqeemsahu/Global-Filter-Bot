from aiogram import types
from database.db import load_filters
from config.config import HOW_TO_WATCH_LINK

def register_handlers(dp):

    @dp.inline_handler()
    async def inline_search(query: types.InlineQuery):
        text = query.query.lower()
        filters = load_filters()
        results = []

        for name, data in filters.items():
            if text in name.lower():
                results.append(
                    types.InlineQueryResultArticle(
                        id=name,
                        title=name,
                        description="Send Anime Filter",
                        thumb_url=data["sticker"],
                        input_message_content=types.InputTextMessageContent(
                            message_text=f"🎴 *{name}*",
                            parse_mode="Markdown"
                        ),
                        reply_markup=types.InlineKeyboardMarkup().add(
                            types.InlineKeyboardButton("Join Channel", url=data['channel']),
                            types.InlineKeyboardButton("How to Watch", url=HOW_TO_WATCH_LINK)
                        )
                    )
                )

        await query.answer(results, cache_time=1)
