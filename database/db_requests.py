from database.models import async_session
from database.models import Users, Categories_food, Categories_gym, Foods, Gyms, Water_norm
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError



async def reg_user(chat_id, fullname) -> bool:
    """Первая регистрация пользователя"""
    async with async_session() as session:
        user = await session.scalar(select(Users).where(Users.tg_id == chat_id))

        if not user:
            session.add(Users(tg_id=chat_id, full_name=fullname))
            await session.commit()
            return False
        else:
            return True


async def check_user_kbju(chat_id):
    """Проверка на наличие кбжу"""
    async with async_session() as session:
        user = await session.scalar(select(Users).where(Users.tg_id == chat_id))
        return user




"""Расчет калорий с занесением в БД"""
async def calorie_calculation(chat_id, age, weight, height):
    async with async_session() as session:

       stmt = (
           update(Users).values(age=age, weight=weight, height=height, kbju=(10*weight+6.25*height-5*age+5)).filter_by(tg_id=chat_id)
       )
       await session.execute(stmt)
       await session.commit()

"""Функция запроса из БД Категорий еды"""
async def get_categories_foods():
    async with async_session() as session:
        return await session.scalars(select(Categories_food))


"""Функция запроса из БД Категорий тренировок"""
async def get_categories_gyms():
    async with async_session() as session:
        return await session.scalars(select(Categories_gym))


"""Функция запроса из БД названия еды"""
async def get_products_by_category(cat_food_id):
    async with async_session() as session:
        return await session.scalars(select(Foods).where(Foods.id_categories_food == cat_food_id))

"""Функция запроса из БД конкретного блюда со всеми столбцами"""
async  def get_products(product_id):
    async with async_session() as session:
        return await session.scalar(select(Foods).where(Foods.foods_id == product_id))

"""Функция запроса из БД названия тренировок"""
async def get_exercise_by_category(cat_gym_id):
    async with async_session() as session:
        return await session.scalars(select(Gyms).where(Gyms.id_categories_gym == cat_gym_id))


async def db_get_water_norm(chat_id):
    async with async_session() as session:
        try:
            subquery = await session.scalar(select(Users).where(Users.tg_id == chat_id))
            query = Water_norm(user_id=subquery.id)
            session.add(query)
            await session.commit()
        except IntegrityError:
            await session.rollback()






"""Функция запроса из БД конкретного упражнения со всеми столбцами"""
async  def get_exercise(exercise_id):
    async with async_session() as session:
        return await session.scalar(select(Gyms).where(Gyms.gyms_id == exercise_id))





