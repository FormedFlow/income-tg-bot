from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from config import base_settings_sync


stmt = text("SELECT 'hello world';")

engine = create_engine(base_settings_sync.conn_string, echo=True)
with Session(engine) as session:
    res = session.execute(statement=stmt)
    for row in res:
        print(row)

