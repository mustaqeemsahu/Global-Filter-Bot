from aiogram import types
from config.config import ADMINS
from database.db import load_filters, save_filters

def register_handlers(dp):

    @dp.message_handler(commands=['add'])
    async def add_filter(message: types.Message):
        if message.from_user.id not in ADMINS:
            return
        
        try:
            _, name, sticker, channel = message.text.split(maxsplit=3)
            filters = load_filters()
            filters[name] = {"sticker": sticker, "channel": channel}
            save_filters(filters)
            await message.reply(f"✅ Added filter **{name}**")
        except:
            await message.reply("❌ Usage:\n/add <name> <sticker_id> <channel_url>")

    @dp.message_handler(commands=['delete'])
    async def delete_filter(message: types.Message):
        if message.from_user.id not in ADMINS:
            return
        
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

    @dp.message_handler(commands=['list'])
    async def list_filters(message: types.Message):
        if message.from_user.id not in ADMINS:
            return
        
        filters = load_filters()
        text = "📚 **Anime List:**\n\n" + "\n".join(filters.keys())
        await message.reply(text, parse_mode="Markdown")
