import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

API_TOKEN = '7613382979:AAGFqEcfI9kw4x0TJEofb1sJXBT5BlyTfDw'
ADMIN_ID = 5056326003  # O'z Telegram ID'ingizni yozing

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# --- Holatlar ---
class Order(StatesGroup):
    waiting_for_name = State()
    waiting_for_pubg_id = State()
    waiting_for_uc_amount = State()
    waiting_for_check = State()

# --- /start ---
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer("👋 Salom! UC buyurtma berish uchun ismingizni va familiyangizni kiriting:")
    await Order.waiting_for_name.set()

# --- Ismni olish ---
@dp.message_handler(state=Order.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("🆔 PUBG ID raqamingizni kiriting:")
    await Order.waiting_for_pubg_id.set()

# --- PUBG ID ---
@dp.message_handler(state=Order.waiting_for_pubg_id)
async def process_pubg_id(message: types.Message, state: FSMContext):
    await state.update_data(pubg_id=message.text)

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("60 UC - 14 000 so'm", "325 UC - 65 000 so'm")
    markup.add("660 UC - 120 000 so'm", "1800 UC - 287 000 so'm")
    markup.add("3850 UC - 570 000 so'm", "8100 UC - 1.150000 so'm")

    await message.answer(
        "💰 Qancha UC sotib olmoqchisiz?\nNarxlar quyidagicha:",
        reply_markup=markup
    )
    await Order.waiting_for_uc_amount.set()

# --- UC tanlash ---
@dp.message_handler(state=Order.waiting_for_uc_amount)
async def process_uc_amount(message: types.Message, state: FSMContext):
    await state.update_data(uc_amount=message.text)

    await message.answer(
        "✅ Endi to‘lovni amalga oshiring va to‘lov chekini skrinshot qilib yuboring.\n\n"
        "💳 To‘lov uchun karta: 8600 1234 5678 9101\n"
        "👤 Ism: Bot Admin\n\n"
        "Chekni rasm (screenshot) ko‘rinishida yuboring:",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await Order.waiting_for_check.set()

# --- Chek rasmni qabul qilish ---
@dp.message_handler(content_types=types.ContentType.PHOTO, state=Order.waiting_for_check)
async def process_check(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user = message.from_user

    caption = (
        f"🛒 *Yangi UC buyurtma!*\n\n"
        f"👤 *Ismi:* {data['name']}\n"
        f"🔰 *Username:* @{user.username or 'yo‘q'}\n"
        f"🆔 *PUBG ID:* {data['pubg_id']}\n"
        f"💎 *Tanlangan UC:* {data['uc_amount']}\n\n"
        f"📎 *To‘lov cheki quyida*"
    )

    # Inline tugmalar
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("✅ Qabul qilish", callback_data=f"accept_{user.id}"),
        InlineKeyboardButton("❌ Rad etish", callback_data=f"reject_{user.id}")
    )

    await bot.send_photo(
        chat_id=ADMIN_ID,
        photo=message.photo[-1].file_id,
        caption=caption,
        parse_mode="Markdown",
        reply_markup=keyboard
    )

    await message.answer("✅ Buyurtmangiz adminga yuborildi. Tez orada UC hisobingizga tushiriladi.")
    await state.finish()

# --- Admin tugmalariga javob ---
@dp.callback_query_handler(lambda c: c.data.startswith(('accept_', 'reject_')))
async def handle_admin_decision(callback_query: types.CallbackQuery):
    decision, user_id = callback_query.data.split('_')
    user_id = int(user_id)

    if decision == "accept":
        await bot.send_message(chat_id=user_id, text="✅ To‘lov tasdiqlandi. UC tez orada hisobingizga tushiriladi.")
        await callback_query.message.edit_reply_markup()
        await callback_query.answer("Buyurtma qabul qilindi.")
    elif decision == "reject":
        await bot.send_message(chat_id=user_id, text="❌ Kechirasiz, to‘lov rad etildi. Iltimos, tekshirib qayta yuboring.")
        await callback_query.message.edit_reply_markup()
        await callback_query.answer("Buyurtma rad etildi.")

# --- Botni ishga tushirish ---
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
