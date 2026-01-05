from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from sync_config import settings


stmt = text("SELECT 'hello world';")

engine = create_engine(settings.conn_string, echo=True)
with Session(engine) as session:
    res = session.execute(statement=stmt)
    for row in res:
        print(row)
