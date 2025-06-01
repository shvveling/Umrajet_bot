from aiogram import Bot, Dispatcher, types, executor
from config import BOT_TOKEN, ADMINS

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer(
        "🕋 *UmraJet Premium botga xush kelibsiz!*

"
        "Iltimos, quyidagi tillardan birini tanlang:

"
        "🇺🇿 O‘zbekcha
🇸🇦 Arabic
🇷🇺 Русский
🇬🇧 English",
        parse_mode='Markdown'
    )

@dp.message_handler(commands=['admin'])
async def admin_handler(message: types.Message):
    if message.from_user.username in ADMINS:
        await message.answer("✅ Siz adminsiz.")
    else:
        await message.answer("⛔ Siz admin emassiz.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
