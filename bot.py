import json
import logging
from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN, ADMINS, HOW_TO_WATCH_LINK
from database import load_filters, save_filters

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


### ------------ INLINE MODE ---------------- ###
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
                        message_text=f"🎴 *{name}*\n\nJoin Channel: {data['channel']}",
                        parse_mode="Markdown"
                    ),
                    reply_markup=types.InlineKeyboardMarkup().add(
                        types.InlineKeyboardButton("Join Channel", url=data['channel']),
                        types.InlineKeyboardButton("How to Watch", url=HOW_TO_WATCH_LINK)
                    )
                )
            )

    await query.answer(results, cache_time=1)


### ------------ COMMAND: /anime <name> ---------------- ###
@dp.message_handler(commands=['anime'])
async def anime_filter(message: types.Message):
    text = message.text.split(maxsplit=1)

    if len(text) != 2:
        return await message.reply("❌ Usage: `/anime <name>`", parse_mode="Markdown")

    search = text[1].lower()
    filters = load_filters()

    for name, data in filters.items():
        if search == name.lower():
            kb = types.InlineKeyboardMarkup()
            kb.add(
                types.InlineKeyboardButton("Join Channel", url=data['channel']),
                types.InlineKeyboardButton("How to Watch", url=HOW_TO_WATCH_LINK)
            )

            await bot.send_sticker(message.chat.id, data["sticker"])
            return await bot.send_message(
                message.chat.id,
                f"**{name}**",
                parse_mode="Markdown",
                reply_markup=kb
            )

    await message.reply("❌ No Filter Found!")


### ------------ ADMIN COMMANDS ---------------- ###

@dp.message_handler(commands=['add'], user_id=ADMINS)
async def add_filter(message: types.Message):
    try:
        _, name, sticker, channel = message.text.split(maxsplit=3)

        filters = load_filters()
        filters[name] = {"sticker": sticker, "channel": channel}
        save_filters(filters)

        await message.reply(f"✅ Added filter **{name}**")
    except:
        await message.reply("❌ Usage:\n/add <name> <sticker_file_id> <channel_url>")


@dp.message_handler(commands=['delete'], user_id=ADMINS)
async def delete_filter(message: types.Message):
    try:
        _, name = message.text.split(maxsplit=1)

        filters = load_filters()
        if name in filters:
            del filters[name]
            save_filters(filters)
            return await message.reply(f"🗑 Deleted **{name}**")

        await message.reply("❌ Filter Not Found")
    except:
        await message.reply("❌ Usage:\n/delete <name>")


@dp.message_handler(commands=['list'], user_id=ADMINS)
async def list_filters(message: types.Message):
    filters = load_filters()
    text = "📚 **Anime List:**\n\n" + "\n".join(filters.keys())
    await message.reply(text, parse_mode="Markdown")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
