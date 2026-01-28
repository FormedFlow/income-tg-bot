from fucking_around import user_table, address_table, Address, User
from config import test_settings
from sqlalchemy import create_engine
from sqlalchemy import update, select
from sqlalchemy.orm import Session


engine = create_engine(test_settings.db_url_test)
with Session(engine) as session:
    stmt = (
        update(user_table)
        .where(user_table.c.name == "мужик")
        .values(name="мужичок")
    )
    print(stmt)
    session.execute(stmt)
    session.commit()

    subq = (
        select(address_table.c.email_address)
        .where(user_table.c.id == address_table.c.user_id)
        .where(user_table.c.name == 'бабинс')
        .scalar_subquery()
    )

    stmt_2 = (
        update(user_table)
        .where(user_table.c.name == 'бабинс')
        .values(fullname=subq)
    )

    print("#"*20)
    print(stmt_2)

    print("#"*20)

    