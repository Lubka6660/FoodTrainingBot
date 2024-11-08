from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, Session
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, BigInteger, Integer, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///sqlite3.db')

async_session = async_sessionmaker(engine)

class Base(DeclarativeBase):
    pass

class Users(Base):
    """База пользователей"""

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger, unique=True)
    full_name: Mapped[str] = mapped_column(String(45))
    age: Mapped[int] = mapped_column(nullable=True)
    weight: Mapped[int] = mapped_column(nullable=True)
    height: Mapped[int] = mapped_column(nullable=True)
    kbju: Mapped[int] = mapped_column(nullable=True)

    # def __str__(self):
    #     return self.full_name


class Categories_food(Base):

    """База категорий еды"""

    __tablename__ = 'categories_food'

    id: Mapped[int] = mapped_column(primary_key=True)
    name_categories_food: Mapped[str] = mapped_column(String(50))


    #foods: Mapped[List["Foods"]] = relationship(back_populates="food")

    # def __str__(self):
    #     return str(self.id_categories_food)


class Foods(Base):

    """База еды"""

    __tablename__ = 'foods'

    foods_id: Mapped[int] = mapped_column(primary_key=True)
    name_foods: Mapped[str] = mapped_column(String(50))
    discription_foods: Mapped[str]
    image_path: Mapped[str] = mapped_column(String(100))
    id_categories_food: Mapped[int] = mapped_column(ForeignKey('categories_food.id'))

    #food = relationship("Categories_food", back_populates='foods')


    # def __str__(self):
    #     return str(self.foods_id)


class Categories_gym(Base):

    """База категорий тренировок"""

    __tablename__ = 'categories_gym'

    id: Mapped[int] = mapped_column(primary_key=True)
    name_categories_gym: Mapped[str] = mapped_column(String(50))

    #ym_1 = relationship('Gyms', back_populates='gym_2')

    # def __str__(self):
    #     return str(self.id_categories_gym)

class Gyms(Base):

    """База тренировок"""

    __tablename__ = 'gyms'

    gyms_id: Mapped[int] = mapped_column(primary_key=True)
    name_gyms: Mapped[str] = mapped_column(String(50))
    discription_gyms: Mapped[str]
    video_path: Mapped[str] = mapped_column(String(100))
    id_categories_gym: Mapped[int] = mapped_column(ForeignKey('categories_gym.id'))

    #gym_2 = relationship('Categories_gym', back_populates='gym_1')

    # def __str__(self):
    #     return str(self.gyms_id)


class Water_norm(Base):

    """База нормы воды"""

    __tablename__ = 'water_norm'

    id: Mapped[int] = mapped_column(primary_key=True)
    monday: Mapped[bool] = mapped_column(default=False)
    tuesday: Mapped[bool] = mapped_column(default=False)
    wednesday: Mapped[bool] = mapped_column(default=False)
    thursday: Mapped[bool] = mapped_column(default=False)
    friday: Mapped[bool] = mapped_column(default=False)
    saturday: Mapped[bool] = mapped_column(default=False)
    sunday: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True)


async def async_main(): # Функция которая создает все эти таблицы, если они не существуют в БД
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # categories_gym = ('Тренировка рук', 'Тренировка ног', 'Тренировка спины', 'Тренировка плеч', 'Тренировка пресса')
    # categories_food = ('Завтраки', 'Обеды', 'Ужины', 'Перекусы')
    # gyms = (
    #     (1,'Бицепс', 'Поднятие гантелей к себе', 'url=https//google.com',),
    #     (1, 'Трицепс', 'Поднятие гантелей от себя', 'url=https//google.com', ),
    #     (1, 'Плечелучевая', 'Поднятие гантелей в сторону', 'url=https//google.com',),
    #     (2, 'Четырехглавая', 'Присяд со штангой', 'url=https//google.com',),
    #     (2, 'Икроножная', 'Подъем на носки на скамье', 'url=https//google.com',),
    #     (2, 'Двухглавая', 'Выпрыгивая с положения сидя', 'url=https//google.com',),
    # )
    #
    # foods = (
    #     (1, 'Шакшука', 'Яичница с овощами', 'media/img/shakshuka.jpg',),
    #     (1, 'Геркулес', 'Овсяная каша на воде', 'media/img/gerkules.jpg',),
    #     (1, 'Тосты', 'Тосты с рыбой и чаем', 'media/img/tosti.jpg',),
    #     (4, 'Яблоко', 'Зеленое яблоко 200г', 'media/img/apple.jpg',),
    #     (4, 'Орехи', 'Кешью 150г', 'media/img/keshyu.jpg',),
    #     (4, 'Йогурт', 'Натуральный йогурт TEOS 150г', 'media/img/yogurt.jpg',),
    # )
    #
    # async with async_session() as session:
    #     for category_gym in categories_gym:
    #         query_jym = Categories_gym(name_categories_gym=category_gym)
    #         session.add(query_jym)
    #         await session.commit()
    #
    #     for category_food in categories_food:
    #         query_food = Categories_food(name_categories_food=category_food)
    #         session.add(query_food)
    #         await session.commit()
    #
    #     for gym in gyms:
    #         query = Gyms(
    #             id_categories_gym=gym[0],
    #             name_gyms=gym[1],
    #             discription_gyms=gym[2],
    #             video_path=gym[3]
    #         )
    #         session.add(query)
    #         await session.commit()
    #
    #     for food in foods:
    #         query = Foods(
    #             id_categories_food=food[0],
    #             name_foods=food[1],
    #             discription_foods=food[2],
    #             image_path=food[3]
    #         )
    #         session.add(query)
    #         await session.commit()



