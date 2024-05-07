from pydantic_settings import BaseSettings


class Bot(BaseSettings):
    token: str
    username: str


class Postgres(BaseSettings):
    host: str
    port: int
    db: str
    user: str
    password: str

    def make_connection_string(self) -> str:
        result = (
            f"postgresql+asyncpg://"
            f"{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
        )
        return result


class Redis(BaseSettings):
    host: str
    port: int
    db: int

    def make_connection_string(self) -> str:
        return f"redis://{self.host}:{self.port}/{self.db}"


class Config(BaseSettings):
    bot: Bot
    postgres: Postgres
    redis: Redis
    admin: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "_"


def load_config(env_file="../.env") -> Config:
    config = Config(_env_file=env_file)
    return config
