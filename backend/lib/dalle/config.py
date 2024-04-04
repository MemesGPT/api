import pydantic


class DalleConfig(pydantic.BaseSettings):
    """Конфиги для Dalle."""

    default_model: str = "dall-e-3"
    default_size: str = "1024x1024"
    default_quality: str = "standard"
    default_n: int = 1
