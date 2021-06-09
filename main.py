# pip install requests
import requests
import datetime # для работы с датой и временем
# импортируем токен от Open Weather API
from config import open_weather_api_token
# импорт библиотеки pprint для красивого вывода JSON-ответа
from pprint import pprint


# Функция для получения информации о погоде с сайта https://openweathermaps.org
def get_weather(city, open_weather_api_token):

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
    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_api_token}&units=metric&lang=RU"
        )
        data = r.json()
        # print(data)
        # pprint(data)

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
        print(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"Погода в городе: {city}\nТемпература: {cur_weather}°C {wd}\n"
              f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/сек.\n"
              f"Восход солнца: {sunrise_timestamp.strftime('%Y-%m-%d %H:%M')}\nЗакат солнца: {sunset_timestamp.strftime('%Y-%m-%d %H:%M')}\nПродолжительность дня: {length_of_the_day}\n"
              f"Хорошего дня!")
    except Exception as ex:
        print(ex)
        print("Проверьте название города:")


def main():
    # Запрос данных о городе
    city = input("Введите город: ")
    get_weather(city, open_weather_api_token)


if __name__ == '__main__':
    main()