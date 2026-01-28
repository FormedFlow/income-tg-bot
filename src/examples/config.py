from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: str
    db_url_base: str
    model_config = SettingsConfigDict(env_file='.env', 
                                      env_file_encoding='utf-8',
                                      extra='ignore')
    
class TestSettings(BaseSettings):
    bot_token: str
    db_url_test: str
    model_config = SettingsConfigDict(env_file='.env',
                                      env_file_encoding='utf-8',
                                      extra='ignore')
    

base_settings = Settings()
test_settings = TestSettings()