import telebot
from pyowm import OWM
from pyowm.utils.config import get_default_config


def main():
    bot = telebot.TeleBot("6250780027:AAF3ToS6vFW6sqwGhMtp0XccFPnP6tOvyqQ")

    @bot.message_handler(commands=["start"])
    def start(message):
        bot.send_message(message.chat.id, "Этот бот скажет вам погоду в любом городе. Для этого напишите: погода")

    def get_weather(message):

        language = get_default_config()
        language["language"] = "ru"
        owm = OWM('23232775d430e5fe2ac9a9c2cbdb8410', language)

        manager = owm.weather_manager()
        try:
            city = message.text
            place = manager.weather_at_place(city)

            weather = place.weather
            result_of_weather = f"""
Сейчас на улице: {weather.detailed_status}
Облачность: {weather.clouds}%
Текущая температура: {weather.temperature("celsius").get("temp")} градусов
Максимальная температура: {weather.temperature("celsius").get("temp_max")} градусов
Минимальная температура: {weather.temperature("celsius").get("temp_min")} градусов
Сейчас ощущается: {weather.temperature("celsius").get("feels_like")} градусов
Скорость ветра: {weather.wind()["speed"]}м/c
"""
            bot.send_message(message.chat.id, result_of_weather)
        except:
            bot.send_message(message.chat.id, "Некорректный ввод города((\nВведите город:")
            bot.register_next_step_handler(message, get_weather)



    @bot.message_handler()
    def answers(message):
        if message.text.lower() == "погода":
            bot.send_message(message.chat.id, "Введите город: ")
            bot.register_next_step_handler(message, get_weather)
        else:
            bot.send_message(message.chat.id, "Я не знаю такой команды😞")


    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()