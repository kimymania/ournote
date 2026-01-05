from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "OurNote"
    version: str = "0.1.0"
    api_v1_url: str = "/api/v1"
    port: int = 8000
    jwt_secret_key: str = ""
    jwt_algorithm: str = "HS256"
    jwt_exp_time: int = 15

    model_config = SettingsConfigDict(env_file=".env")
    # POSTGRES_SERVER: str
    # POSTGRES_PORT: int = 5432
    # POSTGRES_USER: str
    # POSTGRES_PASSWORD: str = ""
    # POSTGRES_DB: str = ""

    # @computed_field  # type: ignore[prop-decorator]
    # @property
    # def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
    #     return PostgresDsn.build(
    #         scheme="postgresql+psycopg",
    #         username=self.POSTGRES_USER,
    #         password=self.POSTGRES_PASSWORD,
    #         host=self.POSTGRES_SERVER,
    #         port=self.POSTGRES_PORT,
    #         path=self.POSTGRES_DB,
    #     )


settings = Settings()
