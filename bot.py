# UmraJet Telegram Bot (faqat O'zbek tili)
# Premium to'liq versiya - bot.py (yakuniy versiya)

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import logging
import os
from dotenv import load_dotenv

# === LOAD ENV ===
load_dotenv()
API_TOKEN = os.getenv('BOT_TOKEN')
GROUP_CHAT_ID = int(os.getenv('GROUP_CHAT_ID'))
ADMINS = ['@vip_arabiy', '@V001VB']
CHANNELS = ['@umrajet', '@the_ravza']

CARD_INFO = """
💳 <b>To'lov uchun kartalar:</b>

🇺🇿 UZCARD:
1️⃣ 8600 0304 9680 2624 (Khamidov Ibodulloh)
2️⃣ 5614 6822 1222 3368 (Khamidov Ibodulloh)

🇺🇿 HUMO:
🔢 9860 1001 2621 9243 (Khamidov Ibodulloh)

🌍 VISA:
💳 4140 8400 0184 8680
💳 4278 3100 2389 5840

💰 Krypto:
USDT (TRC20): TLGiUsNzQ8n31x3VwsYiWEU97jdftTDqT3
ETH (BEP20): 0xa11fb72cc1ee74cfdaadb25ab2530dd32bafa8f8
BTC (BEP20): 0xa11fb72cc1ee74cfdaadb25ab2530dd32bafa8f8

🧾 To‘lovni amalga oshirgach, albatta chekni yuboring.
"""

# === LOGGING ===
logging.basicConfig(level=logging.INFO)

# === INIT ===
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# === HOLATLAR ===
class OrderState(StatesGroup):
    waiting_for_service = State()
    waiting_for_quantity = State()
    waiting_for_contact = State()

# === MENU ===
def main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("📋 Xizmatlar", "📦 Buyurtma berish")
    kb.add("ℹ️ Biz haqimizda", "📞 Bog'lanish")
    kb.add("💳 To'lov qilish", "🙏 Donat qilish")
    return kb

# === START ===
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    text = """
🕋 <b>Assalomu alaykum!</b>

🎉 <b>UmraJet</b> — Umra safarini osonlashtiruvchi premium xizmatlar boti!

✅ Vizalar, 🕌 Tasreh, 🚄 HHR Train chiptalari
✅ Ovqatlar, 🍽 Guruhlarga xizmatlar
✅ 💳 Qulay to‘lovlar

📢 Rasmiy kanallar: @umrajet | @the_ravza
👨‍💼 Bog'lanish: @vip_arabiy | @V001VB

👇 Quyidagi menyudan kerakli bo‘limni tanlang:
"""
    await message.answer(text, reply_markup=main_menu(), parse_mode="HTML")

# === XIZMATLAR ===
@dp.message_handler(text="📋 Xizmatlar")
async def services_list(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🕋 Umra Paketlari", callback_data="umra"),
        InlineKeyboardButton("🕌 Ravza Ziyorati", callback_data="ravza"),
        InlineKeyboardButton("🛂 Saudiya Vizalari", callback_data="viza"),
        InlineKeyboardButton("🚄 HHR Poezdlari", callback_data="train"),
        InlineKeyboardButton("🍽 Ovqat Xizmatlari", callback_data="food"),
        InlineKeyboardButton("🙏 Donat", callback_data="donate")
    )
    await message.answer("👇 Quyidagi xizmatlardan birini tanlang:", reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data in ['umra', 'ravza', 'viza', 'train', 'food', 'donate'])
async def service_details(call: types.CallbackQuery):
    info = {
        'umra': """
🕋 <b>Umra Paketlari</b>

• Standart: <b>1200$</b>
• VIP: <b>1800$ dan</b>

✅ Vizalar, mehmonxona, transport va qo‘llab-quvvatlov xizmati kiritilgan.

👨‍💼 @vip_arabiy | @V001VB
📢 @umrajet | @the_ravza
""",
        'ravza': """
🕌 <b>Ravza Ziyorati (Tasreh)</b>

• Vizali: <b>15 SAR/dona</b>
• Vizasiz: <b>20 SAR/dona</b>
• Guruhlarga maxsus narxlar mavjud.

📌 Faqat <b>tasreh</b> xizmatiga vizali/vizasiz farqi mavjud.

👨‍💼 @vip_arabiy | @V001VB
📢 @umrajet | @the_ravza
""",
        'viza': """
🛂 <b>Saudiya Vizalari</b>

• Umra Viza: <b>160$</b>
• Turist Viza: <b>120$</b>
• Guruhlarga maxsus chegirmalar

👨‍💼 @vip_arabiy | @V001VB
📢 @umrajet | @the_ravza
""",
        'train': """
🚄 <b>HHR Poezd Yo‘nalishlari</b>

• Makkah ↔ Madinah
• Makkah ↔ Jeddah ↔ Madinah
• Jeddah ↔ Makkah ↔ Madinah

⏱ Harakat jadvaliga muvofiq chipta bron qilinadi.

👨‍💼 @vip_arabiy | @V001VB
📢 @umrajet | @the_ravza
""",
        'food': """
🍽 <b>Ovqat Xizmatlari</b>

• Guruhlarga alohida menyular
• 3 mahal, yoki to‘plam asosida
• Halol va sifatli ovqatlar

👨‍💼 @vip_arabiy | @V001VB
📢 @umrajet | @the_ravza
""",
        'donate': CARD_INFO
    }
    await call.message.answer(info[call.data], parse_mode="HTML")
    await call.answer()

# === TO'LOV ===
@dp.message_handler(text="💳 To'lov qilish")
async def payment_info(message: types.Message):
    await message.answer(CARD_INFO, parse_mode="HTML")

# === DONAT ===
@dp.message_handler(text="🙏 Donat qilish")
async def donate_info(message: types.Message):
    await message.answer(CARD_INFO, parse_mode="HTML")

# === BIZ HAQIMIZDA ===
@dp.message_handler(text="ℹ️ Biz haqimizda")
async def about_us(message: types.Message):
    text = """
<b>UmraJet — Umra safarini osonlashtiruvchi premium xizmat!</b>

✅ Tezkor xizmat
✅ Tasdiqlangan vizalar
✅ Guruhlarga chegirmalar
✅ Doimiy yordam va maslahat
✅ Xalqaro to‘lovlar

📢 Kanallar: @umrajet | @the_ravza
📞 Bog‘lanish: @vip_arabiy | @V001VB
"""
    await message.answer(text, parse_mode="HTML")

# === BOG'LANISH ===
@dp.message_handler(text="📞 Bog'lanish")
async def contact_info(message: types.Message):
    text = """
💬 <b>Ma'mur bilan bog'lanish:</b>

👤 @vip_arabiy
👤 @V001VB

📢 Kanal: @umrajet
📢 Kanal: @the_ravza
"""
    await message.answer(text, parse_mode="HTML")

# === BUYURTMA BERISH ===
@dp.message_handler(text="📦 Buyurtma berish")
async def order_start(message: types.Message):
    await message.answer("📝 Qaysi xizmatni buyurtma bermoqchisiz? (Masalan: Umra, Ravza, Viza, Ovqat...)")
    await OrderState.waiting_for_service.set()

@dp.message_handler(state=OrderState.waiting_for_service)
async def process_service(message: types.Message, state: FSMContext):
    await state.update_data(service=message.text)
    await message.answer("📦 Buyurtma miqdorini kiriting (nechta?)")
    await OrderState.waiting_for_quantity.set()

@dp.message_handler(state=OrderState.waiting_for_quantity)
async def process_quantity(message: types.Message, state: FSMContext):
    await state.update_data(quantity=message.text)
    await message.answer("📱 Iltimos, telefon raqamingizni yuboring yoki yozing:")
    await OrderState.waiting_for_contact.set()

@dp.message_handler(state=OrderState.waiting_for_contact)
async def process_contact(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    service = user_data['service']
    quantity = user_data['quantity']
    contact = message.text

    text = f"""
📥 <b>Yangi buyurtma:</b>

🧾 Xizmat: {service}
🔢 Miqdori: {quantity}
📱 Kontakt: {contact}
👤 Foydalanuvchi: @{message.from_user.username or 'yo‘q'}
🆔 ID: <code>{message.from_user.id}</code>
"""
    await bot.send_message(GROUP_CHAT_ID, text, parse_mode="HTML")
    await message.answer("✅ Buyurtmangiz qabul qilindi! Tez orada menedjerlar siz bilan bog‘lanadi.", reply_markup=main_menu())
    await state.finish()

# === BOTNI ISHGA TUSHIRISH ===
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
