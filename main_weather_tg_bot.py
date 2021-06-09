import requests
import datetime
from config import tg_bot_token, open_weather_api_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    # Отображение разметки клавиатуры
    keyboard_markup = types.InlineKeyboardMarkup(row_width=3)
    button_show_weather = types.InlineKeyboardButton(text="Показать сводку погоды",callback_data='show_weather')
    keyboard_markup.add(button_show_weather)
    await message.reply("Привет! Для запроса сводки погоды нажми кнопку ниже",reply_markup=keyboard_markup)


@dp.callback_query_handler(text=['show_weather','yes', 'no'])
async def inline_kb_answer_callback_handler(query: types.CallbackQuery):
    answer_data = query.data
    if answer_data == 'show_weather':
        text = "Напиши мне название города и я пришлю сводку погоды!"
    elif answer_data == 'yes':
        text = "Напиши мне название города и я пришлю сводку погоды!"
    else:
        text ="Хорошего дня!"
    await bot.send_message(query.from_user.id, text)

@dp.message_handler()
async def get_weather(message: types.Message):
    # Создадим словарь для описаний погоды того или иного города в виде смайлов
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B",
    }
    keyboard_markup = types.InlineKeyboardMarkup(row_width=3)
    button_again_yes = types.InlineKeyboardButton(text="Да!",callback_data='yes')
    button_again_no = types.InlineKeyboardButton(text="Нет!",callback_data='no')

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_api_token}&units=metric&lang=RU"
        )
        data = r.json()

        # Название города получаем из ответа от сервера
        city = data['name']
        # Забираем информацию о текущей погоде, содержащейся в ответе от сервера
        cur_weather = data["main"]["temp"]
        # Получаем описание погоды из информации, содержащейся в ответе от сервера
        weather_description = data["weather"][0]["main"]
        # Если описание погоды совпадает со значением ключа словаря с эмоджи, то выводим значение словаря
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода!"
        # Забираем информацию о влажности в ответе от сервера
        humidity = data["main"]["humidity"]
        # Забираем информацию о давлении в ответе от сервера
        pressure = data["main"]["pressure"]
        # Забираем информацию о скорости ветра в ответе от сервера
        wind = data["wind"]["speed"]
        # Время рассвета, высчитанное с учётом timestamp UNIX (с 1970 года - года выхода UNIX)
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        # Время заката, высчитанное с учётом timestamp UNIX (с 1970 года - года выхода UNIX)
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        # Продолжительность светового дня
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"]
        )

        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"Погода в городе: {city}\nТемпература: {cur_weather}°C {wd}\n"
              f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/сек.\n"
              f"Восход солнца: {sunrise_timestamp.strftime('%Y-%m-%d %H:%M')}\nЗакат солнца: {sunset_timestamp.strftime('%Y-%m-%d %H:%M')}\nПродолжительность дня: {length_of_the_day}\n")
        keyboard_markup.add(button_again_yes, button_again_no)
        await message.reply("Запросить сводку погоды снова?",reply_markup=keyboard_markup)

    except:
        await message.reply("\U00002620 Проверьте название города\U00002620")

if __name__ == '__main__':
    executor.start_polling(dp)