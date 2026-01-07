from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


metadata_obj = MetaData()
example_one = Table(
    'user',
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('name', String(30)),
    Column('age', Integer)
)

print(repr(example_one.c.name))