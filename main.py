import asyncio
from os import getenv
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InputFile, FSInputFile, URLInputFile
from dotenv import load_dotenv
from database.models import async_main
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database.db_requests import *

from keyboards.inline_kb import *
from keyboards.replay_kb import *


load_dotenv()
TOKEN = getenv('TOKEN')

dp = Dispatcher()
bot = Bot(TOKEN)

class Kalorii(StatesGroup):
    age = State()
    weight = State()
    height = State()





@dp.message(CommandStart())
async def cmd_start_reg(message: Message):
    """Обработчик команды Старт"""

    await message.answer(f'Добро пожаловать, {message.from_user.full_name}!\nВас приветствует Ваш индивидуальный помощник .')
    await start_register_user(message)


async def start_register_user(message: Message):
    """Функция регистрации или авторизации пользователя"""

    chat_id = message.chat.id
    fullname = message.from_user.full_name
    if await reg_user(chat_id, fullname):
        await message.answer('Вы авторизованны', reply_markup=kb_main_menu)
    else:
        await message.answer('Вы зарегестрированны', reply_markup=kb_main_menu)


"""Обработчик кнопки меню  Хочу похудеть!🏃‍ + FSM для расчета кбжу и занесения в БД"""

@dp.message(F.text == 'Хочу похудеть!🏃‍♀️')
async def to_lose_weight(message: Message, state: FSMContext):
    users = await check_user_kbju(message.chat.id)
    if users.kbju != None:
        await message.answer(f'Суточная норма кбжу для вас:{users.kbju}', reply_markup=kb_category)
    else:
        await state.set_state(Kalorii.age)  # Устонавливаем состояние для ввода имени
        await message.answer('Вы выбрали программу похудения, для начало рассчитаем ваше суточное кбжу!')
        await message.answer('Введите Ваше возраст (полных лет)!')

@dp.message(Kalorii.age)
async def kbju_1(message: Message, state: FSMContext):
    await state.update_data(age=int(message.text))  # Сохраняем возраст который прислал пользователь
    await state.set_state(Kalorii.weight)  # Устонавливаем состояние для ввода веса
    await message.answer('Введите Ваш вес в кг!')

@dp.message(Kalorii.weight)
async def kbju_2(message: Message, state: FSMContext):
    await state.update_data(weight=int(message.text))  # Сохраняем вес который прислал пользователь
    await state.set_state(Kalorii.height)  # Устонавливаем состояние для ввода роста
    await message.answer('Введите Ваше рост в см!')

@dp.message(Kalorii.height)
async def kbju_2(message: Message, state: FSMContext):
    await state.update_data(height=int(message.text))  # Сохраняем рост который прислал пользователь
    data = await state.get_data() # Записываем в переменную data всю информацию в виде словаря
    chat_id = message.chat.id
    await calorie_calculation(chat_id, data['age'], data['weight'], data['height'])
    await message.answer(f'Суточная норма кбжу для вас:{(10*data["weight"]+6.25*data["height"]-5*data["age"]+5)}', reply_markup=kb_category)
    await state.clear()



@dp.message(F.text == 'Питание на 7 дней!🥑')
async def get_foods(message: Message):
    """Обработчик кнопки Питание на 7 дней!🥑 """

    await message.answer('Выберите категорию', reply_markup=await categories_food())



@dp.message(F.text == 'Тренировки на 7 дней🏋️‍♂️')
async def get_gyms(message: Message):
    """Обработчик кнопки Тренировки на 7 дней!🥑 """

    await message.answer('Выберите категорию', reply_markup=await categories_gym())


@dp.message(F.text == '⬅ Назад')
async def return_main_menu(message: Message):
    """Оброаботчик кнопки Назад в главное меню"""
    chat_id = message.chat.id
    message_id = message.message_id

    await bot.delete_message(chat_id=chat_id,
                             message_id=message_id)
    await message.answer(text='Выберите пукнт меню', reply_markup=kb_main_menu)





@dp.callback_query(F.data.startswith('cat_food_')) #Обрабатываем callback который начинается на cat_food_
async def category_product(callback: CallbackQuery):
    """Обработчик любой кнопки из категории еды!🥑 """
    chat_id = callback.message.chat.id
    message_id = callback.message.message_id
    await callback.answer('Вы выбрали категорию ')
    await bot.edit_message_text('Выберите блюдо из категории',
                                chat_id=chat_id,
                                message_id=message_id,
                                reply_markup=await products(callback.data.split('_')[2]))


@dp.callback_query(F.data == 'return_to_category_food')
async def return_to_category_food_button(callback: CallbackQuery):
    """Кнопка назад к главному меню"""
    chat_id = callback.message.chat.id
    message_id = callback.message.message_id
    await callback.answer('Вы вернулись к категориям!')
    await bot.edit_message_text(text='Выберите категорию',
                                chat_id=chat_id,
                                message_id=message_id,
                                reply_markup=await categories_food())


@dp.callback_query(F.data.startswith('cat_gym_')) #Обрабатываем callback который начинается на cat_food_
async def category_exercise(callback: CallbackQuery):
    """Обработчик любой кнопки из категории тренировок """
    chat_id = callback.message.chat.id
    message_id = callback.message.message_id
    await callback.answer('Вы выбрали категорию ')
    await bot.edit_message_text('Выберите упражнение из категории',
                                chat_id=chat_id,
                                message_id=message_id,
                                reply_markup=await exercises(callback.data.split('_')[2]))


@dp.callback_query(F.data == 'return_to_category_gym')
async def return_to_category_gym_button(callback: CallbackQuery):
    """Кнопка назад к главному меню"""
    chat_id = callback.message.chat.id
    message_id = callback.message.message_id
    await callback.answer('Вы вернулись к категориям!')
    await bot.edit_message_text(text='Выберите категорию',
                                chat_id=chat_id,
                                message_id=message_id,
                                reply_markup=await categories_gym())


@dp.callback_query(F.data.startswith('product_'))
async def product(callback: CallbackQuery):
    """Обработчик любой кнопки название еды!🥑 """
    chat_id = callback.from_user.id
    message_id = callback.message.message_id
    products_data = await get_products(callback.data.split('_')[1])

    await bot.delete_message(chat_id=chat_id,
                             message_id=message_id)
    await callback.answer('Вы выбрали блюдо!')
    await callback.message.answer_photo(photo=FSInputFile(path=products_data.image_path,),
                                        caption=f'Название:{products_data.name_foods}\nОписание:{products_data.discription_foods}\n', reply_markup=kb_category)




@dp.callback_query(F.data.startswith('exercise_'))
async def product(callback: CallbackQuery):
    """Обработчик любой кнопки название еды!🥑 """
    chat_id = callback.from_user.id
    message_id = callback.message.message_id
    exercise_data = await get_exercise(callback.data.split('_')[1])

    await bot.delete_message(chat_id=chat_id,
                             message_id=message_id)
    await callback.answer('Вы выбрали упражнение!')
    await callback.message.answer(f'Название:{exercise_data.name_gyms}\n Описание:{exercise_data.discription_gyms}\n')
    await callback.message.answer(exercise_data.video_path, reply_markup=kb_category)


@dp.message(F.text == 'Норма воды на 7 дней🍺')
async def get_water_norm(message: Message):
    """Отдаем пользователю норму воды"""

    chat_id = message.from_user.id
    message_id = message.message_id
    await message.answer('Ваша суточная норма воды 1.5 л 💧', reply_markup=inl_kb_water_norm)



@dp.callback_query(F.data == 'drank')
async def reaction_on_drank(callback: CallbackQuery):
    """Отдаем пользователю сколько он выпил за неделю """
    chat_id = callback.from_user.id
    message_id = callback.message.message_id
    await db_get_water_norm(chat_id)

    # await bot.delete_message(chat_id=chat_id,
    #                          message_id=message_id)
    # await callback.answer(f'Вы большой молодец!{water_norm_data.user_id}')





async def main():
    await async_main()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

