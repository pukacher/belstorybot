import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

# === НАСТРОЙКИ ===
API_TOKEN = "7624098941:AAHu_oIJYj4S_vjDWua5_m95PnYJgkKNnMc"
CHANNEL_USERNAME = "@BretelkaSalon"
PDF_FILE_PATH = "Гайд Капсула для отпуска.pdf"

# === ЛОГИ ===
logging.basicConfig(level=logging.INFO)

# === БОТ ===
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# === КНОПКИ ===
def subscribe_button():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Я подписана", callback_data="check_subscribe")],
            [InlineKeyboardButton(text="📢 Подписаться на канал", url="https://t.me/BretelkaSalon")]
        ]
    )

# === СТАРТ ===
@dp.message(Command("start"))
async def start(message: types.Message):
    text = (
        "📍Привет! Мы — сеть магазинов MyBelstory совместно со стилистом Риммой Кулаковой "
        "составили для Вас гайд «В отпуск налегке», который поможет вам собрать летнюю капсулу "
        "для идеального путешествия. Чтобы собрать чемодан без головной боли, не переплачивать "
        "за перевес🤭 и каждый день носить новые образы💃🏼\n\n"
        "Чтобы получить гайд, необходимо подписаться на канал MyBelstory 👇"
    )
    await message.answer(text, reply_markup=subscribe_button())

# === ПРОВЕРКА ПОДПИСКИ ===
async def check_subscription(user_id: int) -> bool:
    member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
    return member.status in ("member", "administrator", "creator")

# === ОБРАБОТКА КНОПКИ ===
@dp.callback_query(F.data == "check_subscribe")
async def check_sub(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if await check_subscription(user_id):
        await callback.message.answer(
            "📍 Отлично! Подписка есть🙌🏻 Лови гайд и отличного тебе отпуска ✈️"
        )
        await callback.message.answer_document(types.FSInputFile(PDF_FILE_PATH))
    else:
        await callback.message.answer(
            "📍Хммм… почему-то я не нашел тебя среди подписчиков. "
            "Давай попробуем еще раз 👇",
            reply_markup=subscribe_button()
        )

# === ЗАПУСК ===
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
