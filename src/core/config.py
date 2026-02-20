from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import ValidationError

ENV_PATH = r'D:\python\telegram_stuff\financial-bot\src\core\.env'


class Settings(BaseSettings):
    bot_token: str
    db_url_test: str
    db_url_base_async: str
    model_config = SettingsConfigDict(env_file=ENV_PATH, 
                                      env_file_encoding='utf-8',
                                      extra='ignore')

base_settings = Settings()