from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton
from database.db_requests import get_categories_foods, get_categories_gyms, get_products_by_category, \
    get_exercise_by_category

"""Клавиатура вывода категорий еды"""
async def categories_food():
    all_categories_food = await get_categories_foods()
    kb_category_food = InlineKeyboardBuilder()
    for cat_food in all_categories_food:
        kb_category_food.add(InlineKeyboardButton(text=cat_food.name_categories_food, callback_data=f'cat_food_{cat_food.id}'))
    return kb_category_food.adjust(2).as_markup()


"""Клавиатура вывода категорий тренировок"""
async def categories_gym():
    all_categories_gym = await get_categories_gyms()
    kb_category_gym = InlineKeyboardBuilder()
    for cat_gym in all_categories_gym:
        kb_category_gym.add(InlineKeyboardButton(text=cat_gym.name_categories_gym, callback_data=f'cat_gym_{cat_gym.id}'))
    return kb_category_gym.adjust(2).as_markup()


"""Клавиатура вывода названия блюда"""
async def products(cat_food_id):
    all_products = await get_products_by_category(cat_food_id)
    kb_products = InlineKeyboardBuilder()
    for product in all_products:
        kb_products.add(InlineKeyboardButton(text=product.name_foods, callback_data=f'product_{product.foods_id}'))
    kb_products.row(InlineKeyboardButton(text='⬅ Назад', callback_data='return_to_category_food'))
    return kb_products.adjust(2, 1).as_markup()

"""Клавиатура вывода названия тренировок"""
async def exercises(cat_gym_id):
    all_exercises = await get_exercise_by_category(cat_gym_id)
    kb_exercises = InlineKeyboardBuilder()
    for exercise in all_exercises:
        kb_exercises.add(InlineKeyboardButton(text=exercise.name_gyms, callback_data=f'exercise_{exercise.gyms_id}'))
    kb_exercises.row(InlineKeyboardButton(text='⬅ Назад', callback_data='return_to_category_gym'))
    return kb_exercises.adjust(2, 1).as_markup()

# url_button_gym = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='Видео упражнения', url=)]
# ])


inl_kb_water_norm = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Выпил ✅', callback_data='drank'), InlineKeyboardButton(text='Не выпил ➖', callback_data='didnt drink')]
])



