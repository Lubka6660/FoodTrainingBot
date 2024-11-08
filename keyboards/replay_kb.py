from aiogram.utils.keyboard import ReplyKeyboardMarkup, ReplyKeyboardBuilder, KeyboardButton

kb_main_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Хочу похудеть!🏃‍♀️'), KeyboardButton(text='Хочу набрать массу!🦾')]
], resize_keyboard=True, input_field_placeholder='Выберите пункт меню!', one_time_keyboard=True)


kb_category = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Питание на 7 дней!🥑'), KeyboardButton(text='Тренировки на 7 дней🏋️‍♂️')],
    [KeyboardButton(text='Норма воды на 7 дней🍺'), KeyboardButton(text='Норма сна на 7 дней')],
    [KeyboardButton(text='⬅ Назад')]
], resize_keyboard=True, input_field_placeholder='Выберите пункт меню!', one_time_keyboard=True)



