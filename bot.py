from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.utils.markdown import hbold
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import F
import aiohttp
import asyncio
import logging

API_TOKEN = '7583712608:AAFZMr_bHyX0JBTNAZBvxk28gUC5_K3glU8'
SMSHUB_API_KEY = '135457U6df9439ad521011cedc614ab5e4405a0'
GETSMS_API_KEY = 'NUESPSUZHA77L9TDNE9BZUF4Y4LF9G3L'

from aiogram.client.default import DefaultBotProperties

bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📲 Купить номер")],
        [KeyboardButton(text="💰 Пополнить")],
    ],
    resize_keyboard=True
)

back_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔙 Назад")],
    ],
    resize_keyboard=True
)

buy_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🌐 SMSHub"), KeyboardButton(text="📡 GetSMS")],
        [KeyboardButton(text="🔙 Назад")],
    ],
    resize_keyboard=True
)

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Привет, {hbold(message.from_user.full_name)}! 👋\nВыбери действие:", reply_markup=main_menu)

@dp.message(F.text == "🔙 Назад")
async def back(message: Message):
    await message.answer("Главное меню:", reply_markup=main_menu)

@dp.message(F.text == "💰 Пополнить")
async def top_up(message: Message):
    text = (
        "<b>💰 Пополнение:</b>\n\n"
        "1️⃣ <b>SMSHub:</b>\n<code>0xeca1f75f8aa7274a2b924ebef435d814465e3c04</code>\n"
        "2️⃣ <b>GetSMS:</b>\n<code>0x0c52bB955DAA8fC1f6AB79E5df8F907563a5Bb7B</code>\n\n"
        "После пополнения свяжитесь с поддержкой."
    )
    await message.answer(text, reply_markup=back_menu)

@dp.message(F.text == "📲 Купить номер")
async def buy_number(message: Message):
    await message.answer("Выберите сервис:", reply_markup=buy_menu)

@dp.message(F.text == "🌐 SMSHub")
async def buy_smshub(message: Message):
    await message.answer("🔄 Запрос номера через SMSHub для KZ...", reply_markup=back_menu)
    async with aiohttp.ClientSession() as session:
        try:
            url = f'https://smshub.org/stubs/handler_api.php?api_key={SMSHUB_API_KEY}&action=getNumber&service=wt&country=2'
            async with session.get(url) as resp:
                text = await resp.text()
                if text.startswith("ACCESS_NUMBER"):
                    parts = text.split(':')
                    number = parts[2]
                    await message.answer(f"✅ Номер: <code>{number}</code>")
                elif "NO_NUMBERS" in text:
                    await message.answer("❌ Ошибка SMSHub: нет доступных номеров.")
                else:
                    await message.answer("❌ Ошибка SMSHub: неожиданный ответ.")
        except Exception as e:
            await message.answer(f"❌ Ошибка запроса SMSHub: {str(e)}")

@dp.message(F.text == "📡 GetSMS")
async def buy_getsms(message: Message):
    await message.answer("🔄 Запрос номера через GetSMS для KZ...", reply_markup=back_menu)
    async with aiohttp.ClientSession() as session:
        try:
            url = f'https://getsms.online/stubs/handler_api.php?api_key={GETSMS_API_KEY}&action=getNumber&service=dt&country=kz'
            async with session.get(url) as resp:
                text = await resp.text()
                if text.startswith("ACCESS_NUMBER"):
                    parts = text.split(':')
                    number = parts[2]
                    await message.answer(f"✅ Номер: <code>{number}</code>")
                elif "NO_NUMBERS" in text:
                    await message.answer("❌ Ошибка GetSMS: нет доступных номеров.")
                else:
                    await message.answer("❌ Ошибка GetSMS: неожиданный ответ.")
        except Exception as e:
            await message.answer(f"❌ Ошибка запроса GetSMS: {str(e)}")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

