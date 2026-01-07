from fucking_around import User, Address, address_table, user_table
from config import test_settings
from sqlalchemy import create_engine, select, text, literal_column, label
from sqlalchemy.orm import Session
from sqlalchemy import func


engine = create_engine(test_settings.db_url_test)

with Session(engine) as session:
    stmt_1 = select(user_table.c.fullname).where(user_table.c.name == 'мужик')
    print(session.execute(stmt_1).first())

    stmt_2 = select(User)
    print(session.execute(stmt_2).all())
    print(session.scalars(stmt_2).first())

    stmt_3 = select(literal_column("'норм_парень'").label('nick'), User.name, User.fullname)
    result_3 = session.execute(stmt_3)
    print(stmt_3.compile())
    for row in result_3:
        print(row.nick, row.name)

    
    stmt_4 = select(User.name, User.fullname).where(
        User.id == 46,
        User.name == 'мужик'
    )
    print(session.execute(stmt_4).first())


    stmt_5 = select(User.fullname).filter_by(name='бабинс')
    print(session.execute(stmt_5).first())


    stmt_6 = select(user_table.c.fullname, address_table.c.email_address).join_from(user_table, address_table).where(
        user_table.c.name == 'бабинс'
    )
    for row in session.execute(stmt_6):
        print(row)


    stmt_7 = select(func.count("*")).select_from(user_table)
    print(session.scalars(stmt_7).first())