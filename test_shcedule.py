from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
import requests
import asyncio
from config import token

bot = Bot(token=token)
dp = Dispatcher()

mon = False
user_id = None

async def btcprice():
    try:
        link = 'https://api.binance.com/api/v3/avgPrice?symbol=BTCUSDT'
        data = requests.get(link).json()
        return f"Цена Биткоина щас: {data.get('price')} баксов"
    except Exception as err:
        return f"Чё-то сломалось, ошибка: {err}"

async def monstart():
    global mon
    while mon:
        if user_id:
            msg = await btcprice()
            await bot.send_message(user_id, msg)
        await asyncio.sleep(5)

@dp.message(Command("start"))
async def hello(message: Message):
    await message.answer("Эй! Я слежу за битком. Пиши /btc чтобы начать, или /stop чтобы хватит.")

@dp.message(Command("btc"))
async def begin(message: Message):
    global mon, user_id
    if not mon:
        mon = True
        user_id = message.chat.id
        await message.answer("Ну всё, смотрю за битком!")
        asyncio.create_task(monstart())
    else:
        await message.answer("Уже слежу, не парься!")

@dp.message(Command("stop"))
async def end(message: Message):
    global mon
    if mon:
        mon = False
        await message.answer("Ладно, больше не слежу.")
    else:
        await message.answer("Да я уже не слежу!")

async def main():
    print("Бот заработал!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
