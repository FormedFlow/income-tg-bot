from sqlalchemy import create_engine, Table, MetaData, insert
from sqlalchemy.orm import Session
from config import test_settings


engine = create_engine(test_settings.db_url_test)
metadata_obj = MetaData()
print(f'MetaData: {metadata_obj}')
user_table = Table('user_account', metadata_obj, autoload_with=engine)
# print(user_table.columns)
# stmt = insert(user_table).values(name='габибов фел', age=28)
# compiled = stmt.compile()
# # print(compiled)
# print(compiled.params)

# with Session(engine) as session:
#     result = session.execute(stmt)
#     session.commit()


# stmt_2 = insert(user_table)
# with Session(engine) as session:
#     result = session.execute(
#         stmt_2,
#         [
#             {'name': 'бабинский феликс', 'age': 28},
#             {'name': 'бабинс дрочёный', 'age': 28}
#         ]
#     )
    # session.commit()


stmt_3 = insert(user_table).values()
print(stmt_3.compile(engine))