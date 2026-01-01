from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: str
    conn_string: str
    model_config = SettingsConfigDict(env_file='.env', 
                                      env_file_encoding='utf-8')


settings = Settings()
print(settings.bot_token)
print(settings.conn_string)