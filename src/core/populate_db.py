from faker import Faker
from faker.providers import emoji, currency
import asyncio
import random
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import async_seshmaker
from providers.custom_providers import EmojiProvider, CurrencyProvider
from core.models import Category, User, Currency, user_category, Transaction


class CategoryContainer:
    # Категории расходов (expenses)
    expense_categories = [
        "Продукты",
        "Рестораны",
        "Доставка еды",
        "Кафе",
        "Транспорт",
        "Такси",
        "Бензин",
        "Общественный транспорт",
        "Аренда жилья",
        "Коммунальные платежи",
        "Интернет и связь",
        "Одежда",
        "Обувь",
        "Здоровье",
        "Аптеки",
        "Спорт и фитнес",
        "Красота и уход",
        "Развлечения",
        "Кино",
        "Игры",
        "Хобби",
        "Образование",
        "Книги",
        "Курсы и тренинги",
        "Подарки",
        "Благотворительность",
        "Путешествия",
        "Отели",
        "Авиабилеты",
        "Страхование",
        "Налоги",
        "Ремонт",
        "Техника и электроника",
        "Дом и мебель",
        "Дети",
        "Домашние животные"
    ]

    # Категории доходов (incomes)
    income_categories = [
        "Зарплата",
        "Фриланс",
        "Подработка",
        "Инвестиции",
        "Дивиденды",
        "Кэшбэк",
        "Подарки",
        "Возврат налогов",
        "Аренда недвижимости",
        "Проценты по вкладам",
        "Продажа вещей",
        "Бизнес",
        "Кешбэк",
        "Бонусы",
        "Премия",
        "Социальные выплаты",
        "Пенсия",
        "Стипендия",
        "Алименты",
        "Наследство"
    ]


async def populate_db():
    pass


def make_categories(faker: Faker) -> list[Category]:
    categories = []
    for name in CategoryContainer.expense_categories:
        category = Category(
            name=name,
            emoji=faker.emoji_with_max_len(5),
            is_income=False
        )
        categories.append(category)
    for name in CategoryContainer.income_categories:
        category = Category(
            name=name,
            emoji=faker.emoji_with_max_len(5),
            is_income=True
        )
        categories.append(category)
    return categories


def make_currencies(faker: Faker, count: int) -> list[Currency]:
    currencies = []
    for i in range(count):
        name, code, symbol = faker.currency_with_symbol()
        currency = Currency(
            name=name,
            code=code,
            symbol=symbol,
            display_precision=faker.pyint(max_value=10)
        )
        currencies.append(currency)
    return currencies
    

def make_users(faker: Faker, count: int) -> list[User]:
    users = []
    for i in range(count):
        tg_user_id = faker.pyint(min_value=int(10e8), max_value=int(10e9)-1)
        name = faker.first_name()
        is_admin = False
        user = User(
            tg_user_id=tg_user_id,
            name=name,
            is_admin=is_admin
        )
        users.append(user)
    return users


def make_user_categories(users: list[User], 
                         categories: list[Category], 
                         max_cats: int):
    stmt = insert(user_category)
    entries = []
    for user in users:
        user_id = user.user_id
        cats_count = random.randint(1, max_cats)
        category_id_list = [cat.category_id for cat in random.sample(categories, k=cats_count)]
        entries.extend([{'user_id': user_id, 'category_id': category_id} for category_id in category_id_list])
    return entries


def make_transactions(
    users: list[User],
):
    
    
    

async def main():
    session = async_seshmaker()
    fake = Faker('ru_RU')
    fake.add_provider(EmojiProvider)
    fake.add_provider(CurrencyProvider)
    categories = make_categories(fake)
    currencies = make_currencies(fake, 10)
    users = make_users(fake, 20)

    session.add_all([*categories, *currencies, *users])
    await session.commit()

    user_categories = make_user_categories(
        users=users,
        categories=categories,
        max_cats=15
    )

    await session.execute(
        insert(user_category),
        user_categories
    )

    await session.commit()
    await session.close()


if __name__ == '__main__':
    asyncio.run(main())