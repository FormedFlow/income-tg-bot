from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy import insert
from config import test_settings


engine = create_engine(test_settings.db_url_test)
metadata_obj = MetaData()
user_table = Table('user_account', metadata_obj, autoload_with=engine)
