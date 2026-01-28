from sqlalchemy import create_engine, insert, select, text, func
from sqlalchemy import String, ForeignKey, MetaData, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.orm import Session
from config import test_settings


engine = create_engine(test_settings.db_url_test)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user_account'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[str|None] = mapped_column(String(30), nullable=True)

    addresses: Mapped[list['Address']] = relationship(back_populates='user')

    def __repr__(self):
        return f'id: {self.id}, name: {self.name}, fullname: {self.fullname}'


class Address(Base):
    __tablename__ = 'address'

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str] = mapped_column(String(40))
    user_id = mapped_column(ForeignKey('user_account.id'))

    user: Mapped[User] = relationship(back_populates='addresses')

    def __repr__(self):
        return f'id: {self.id}, email address: {self.email_address}, user_id: {self.user_id}, User: {self.user}'


# print(Address.metadata)
# Address.metadata.create_all(engine)

metadata_obj = MetaData()
user_table = Table('user_account', metadata_obj, autoload_with=engine)
address_table = Table('address', metadata_obj, autoload_with=engine)

insert_stmt = insert(user_table)


def main():
    with Session(engine) as session:
        session.execute(
            insert_stmt,
            [
                {'name': 'фел', 'fullname': 'фел бабинский'},
                {'name': 'бабинс', 'fullname': 'фел бабиныч'}
            ])
        # session.commit()


    select_stmt = select(user_table.c.id, user_table.c.name + '@gmail.com')
    insert_stmt = insert(address_table).from_select(
        ["user_id", "email_address"],
        select_stmt
    )
    print(insert_stmt)

    with Session(engine) as session:
        session.execute(insert_stmt)
        # session.commit()


    select_stmt_2 = select(user_table.c['name', 'fullname'])
    with Session(engine) as session:
        for row in session.execute(select_stmt_2):
            print(row)

    select_stmt_3 = select(User).where(User.name == 'бабинс')
    with Session(engine) as session:
        result = session.execute(select_stmt_3)
        for model in result:
            print(model)
        result = session.scalars(select_stmt_3).first()
        print(result)


    with Session(engine) as session:
        plain_sql = text('SELECT * FROM user_account WHERE name = :name')
        result = session.execute(plain_sql, {'name': 'бабинс'})
        print(result.all())


    with Session(engine) as session:
        insert_stmt_2 = insert(user_table)
        result = session.execute(
            insert_stmt_2,
            [
                {'name': 'феликс', 'fullname': 'феликс габибов'},
                {'name': 'мужик', 'fullname': 'мужик с портфелем'}
            ]
        )
        # session.commit()


    with Session(engine) as session:
        select_stmt_4 = select(user_table.c.fullname).where(user_table.c.name == 'мужик')
        result_4 = session.execute(select_stmt_4)
        for row in result_4:
            print(row)

        count = func.count(Address.id)
        result = session.execute(
            select(User.fullname, count.label('addresses'))
            .join(Address)
            .group_by(User.fullname)
            .having(count > 0)
        )
        print('###'*5)
        for row in result:
            print(row)


    
if __name__ == '__main__':
    main()