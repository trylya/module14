from aiogram import Bot, Dispatcher,executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from crud_functions_14_5 import *

import sqlite3

api = '7371378698:AAE8-SNvT1_eV2Wo2-yyl5NIWKie4Z1iUP4'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Информация')
button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Купить')
button3 = KeyboardButton(text='Регистрация')
kb.add (button3)
kb.row(button, button1)
kb.add(button2)

kb2 = InlineKeyboardMarkup()
in_button1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
in_button2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb2.add(in_button1)
kb2.add(in_button2)

kb3 = InlineKeyboardMarkup(resize_keyboard=True)  # покупка продукта
in_button3 = InlineKeyboardButton(text='Product1', callback_data='product_buying')
in_button4 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
in_button5 = InlineKeyboardButton(text='Product3', callback_data='product_buying')
in_button6 = InlineKeyboardButton(text='Product4', callback_data='product_buying')
kb3.row(in_button3, in_button4)
kb3.row(in_button5, in_button6)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler(text='Информация')
async def inform(message):
    await message.answer('Этот бот поможет вам сохранить желаемый вес. Для этого жми на кнопку Рассчитать')


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb2)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;'
                              '\nдля женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Все данные вводите, пожалуйста, целыми числами')
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    result = (10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5)
    result1 = (10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161)
    await message.answer(
        f'При таких параметрах норма калорий: \nдля мужчин {result} ккал в сутки \nдля женщин {result1} ккал в сутки')
    await UserState.weight.set()
    await state.finish()


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for i in get_all_products():
        number = i[0]
        title = i[1]
        description = i[2]
        price = i[3]
        with open (f'.idea/{number}.jpg', 'rb') as img:
            await message.answer_photo(img, caption=f'Название: {title} | Описание: {description} | Цена: {price}')

        await message.answer(text='Выберите продукт для покупки: ', reply_markup=kb3)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')




class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = 1000

@dp.message_handler(text="Регистрация")
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    await state.update_data(username=message.text)
    data = await state.get_data()

    name = is_included(data['username'])
    if name is True:
        await state.update_data(username=message.text)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()
    else:
        await message.answer("Пользователь существует, введите другое имя")
        await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    print(data)
    add_user(data['username'], data['email'], data['age'])
    await message.answer("Регистрация прошла успешно!")
    await state.finish()

@dp.message_handler()
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)