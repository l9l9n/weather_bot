from aiogram import Bot, Dispatcher, types, executor
import requests
from bs4 import BeautifulSoup as bs
from config import TOKEN, USER_AGENT



bot = Bot(TOKEN)
dp = Dispatcher(bot)



@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer('Привет!\nЯ умею парсить погоду!\nНапиши мне город,\nпогоду в котором нужно узнать')


@dp.message_handler(content_types=['text'])
async def weather_info(message: types.Message):
    try:
        headers = USER_AGENT
        response = requests.get(f'https://www.google.com/search?q={message.text} weather&oq={message.text} weather&aqs=chrome.1.69i57j0i512l5j69i60l2.9839j0j7&sourceid=chrome&ie=UTF-8', headers=headers)
        soup = bs(response.text, 'html.parser')
        time = soup.select('#wob_dts')[0].getText().strip()
        precipitation = soup.select('#wob_dc')[0].getText().strip()
        weather = soup.select('#wob_tm')[0].getText().strip()

        result = f""" День недели и время: {time}\nИнформация об осадках: {precipitation}\nТемпература воздуха: {weather} C."""
        await message.answer(result)

    except Exception as ex:
        await message.answer('Я не смог узнать погоду')





if __name__ == '__main__':
    executor.start_polling(dp)