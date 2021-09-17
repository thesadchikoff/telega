import requests
import datetime
import telebot
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import keyboard as kb


bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)
group_id = -1001543854845


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await bot.send_message(message.from_user.id, "Привет! Я успешно запущен. 🤚\nДля того, чтобы узнать сводку о погоде - введи название интересующего тебя города.", reply_markup=kb.markup_requests)


@dp.message_handler(commands=["hi"])
async def start_command(message: types.Message):
    await bot.send_message(message.from_user.id, "Привет! 🤚\nЯ знаю всё о погоде в твоём городе и не только! Напиши мне название города и я отправлю тебе сводку погоды.", reply_markup=kb.markup_requests)



@dp.message_handler(commands=["help"])
async def start_command(message: types.Message):
    await bot.send_message(message.from_user.id, "Список доступных команд:\n/start - запуск бота.\n/hi - альтернативный запуск бота.", reply_markup=kb.markup_requests)

@dp.message_handler()
async def get_weather(message: types.Message):
        code_to_smile = {
            "Clear": "Ясно \U00002600",
            "Clouds": "Облачно \U0001F325",
            "Rain": "Дождь \U00002614",
            "Drizzle": "Дождь \U00002614",
            "Thunderstorm": "Гроза \U000026A1",
            "Snow": "Снег \U0001F328",
            "Mist": "Туман \U0001F32B",
        }


        try:
            r = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
            )
            data = r.json()

            city = data["name"]
            cur_weather = data["main"]["temp"]
            weather_description = data["weather"][0]["main"]
            if weather_description in code_to_smile:
                wd = code_to_smile[weather_description]
            else:
                wd = "Посмотри в окно, не пойму что там за погода..."
            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            wind = data["wind"]["speed"]
            sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
            sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
            length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

            await message.reply(f"Сводка по погоде в выбранном вами городе:\n\n\U0001F3D9 Погода в городе: {city}\n🌡 Температура: {cur_weather}°\nНа улице сейчас: {wd}\n💧 Влажность: {humidity}%\n🌀 Давление: {pressure} мм.рт.ст\n🌬 Ветер: {wind} м/с\n\U0001F305Восход солнца: {sunrise_timestamp}\n\U0001F307Закат солнца: {sunset_timestamp}\n🕗 Продолжительность дня: {length_of_the_day} часа(ов)\n\n Хорошего дня! ☺ ")

        except:
            await message.reply("🚫 Город не найден, попробуйте указать другой! 🚫")

if __name__ == '__main__':
    executor.start_polling(dp)
