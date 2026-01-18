from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, selectinload, joinedload
from fucking_around import User, Address
from config import test_settings


engine = create_engine(test_settings.db_url_test)
with Session(engine) as session:
    result = session.execute(
        select(Address).options(joinedload(Address.user, innerjoin=True))
    ).all()
    for row in result:
        print(row)
    print('##########'*5)
    u1 = session.get(User, 1)
    print(u1.addresses)