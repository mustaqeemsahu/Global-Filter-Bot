from aiogram import types
from database.db import load_filters
from config.config import HOW_TO_WATCH_LINK

def register_handlers(dp):

    @dp.message_handler(commands=['anime'])
    async def anime_filter(message: types.Message):
        text = message.text.split(maxsplit=1)

        if len(text) != 2:
            return await message.reply("❌ Usage: /anime <name>")

        search = text[1].lower()
        filters = load_filters()

        for name, data in filters.items():
            if search == name.lower():

                kb = types.InlineKeyboardMarkup()
                kb.add(
                    types.InlineKeyboardButton("Join Channel", url=data["channel"]),
                    types.InlineKeyboardButton("How to Watch", url=HOW_TO_WATCH_LINK)
                )

                await message.bot.send_sticker(message.chat.id, data["sticker"])
                return await message.bot.send_message(
                    message.chat.id,
                    f"**{name}**",
                    parse_mode="Markdown",
                    reply_markup=kb
                )

        await message.reply("❌ No Filter Found!")
