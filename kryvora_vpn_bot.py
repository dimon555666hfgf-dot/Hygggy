import os
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Вставь токен BotFather в переменную окружения BOT_TOKEN.
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("Не задан BOT_TOKEN. Добавь токен в переменные окружения.")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

WELCOME = (
    "⚡ <b>KRYVORA VPN</b>\n\n"
    "Добро пожаловать!\n"
    "Быстрый и удобный VPN для Android и iPhone.\n\n"
    "Выбери нужное действие 👇"
)

def main_menu():
    kb = InlineKeyboardBuilder()
    kb.button(text="🛒 Купить VPN", callback_data="buy")
    kb.button(text="🔑 Мой VPN", callback_data="account")
    kb.button(text="🔄 Продлить", callback_data="renew")
    kb.button(text="👥 Пригласить друга", callback_data="referral")
    kb.button(text="🎧 Техническая поддержка", callback_data="support")
    kb.adjust(1)
    return kb.as_markup()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(WELCOME, reply_markup=main_menu(), parse_mode="HTML")

@dp.message(Command("menu"))
async def menu(message: Message):
    await message.answer(WELCOME, reply_markup=main_menu(), parse_mode="HTML")

@dp.callback_query(F.data == "buy")
async def buy(callback: CallbackQuery):
    await callback.message.answer(
        "🛒 <b>Покупка KRYVORA VPN</b>\n\n"
        "Тарифы скоро появятся. Сейчас подключается система оплаты и выдачи доступа.",
        parse_mode="HTML",
        reply_markup=main_menu()
    )
    await callback.answer()

@dp.callback_query(F.data == "account")
async def account(callback: CallbackQuery):
    await callback.message.answer(
        "🔑 <b>Мой VPN</b>\n\n"
        "У тебя пока нет подключённой подписки.\n"
        "Когда подключим H1Cloud, здесь будут отображаться твой ключ и срок действия.",
        parse_mode="HTML",
        reply_markup=main_menu()
    )
    await callback.answer()

@dp.callback_query(F.data == "renew")
async def renew(callback: CallbackQuery):
    await callback.message.answer(
        "🔄 <b>Продление подписки</b>\n\n"
        "Продление станет доступно после подключения системы подписок.",
        parse_mode="HTML",
        reply_markup=main_menu()
    )
    await callback.answer()

@dp.callback_query(F.data == "referral")
async def referral(callback: CallbackQuery):
    me = await bot.get_me()
    link = f"https://t.me/{me.username}?start=ref_{callback.from_user.id}"
    await callback.message.answer(
        "👥 <b>Приглашай друзей в KRYVORA VPN!</b>\n\n"
        f"Твоя ссылка:\n{link}\n\n"
        "Учёт приглашений и бонусы подключим следующим этапом.",
        parse_mode="HTML",
        reply_markup=main_menu()
    )
    await callback.answer()

@dp.callback_query(F.data == "support")
async def support(callback: CallbackQuery):
    await callback.message.answer(
        "🎧 <b>Техническая поддержка</b>\n\n"
        "Опиши свою проблему одним сообщением. "
        "Пока поддержка не подключена к оператору, бот не пересылает сообщения.",
        parse_mode="HTML",
        reply_markup=main_menu()
    )
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
