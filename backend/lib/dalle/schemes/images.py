import pydantic

import lib.dalle.config as dalle_configs

dalle_config = dalle_configs.DalleConfig()


class ImagesGenerateScheme(pydantic.BaseModel):
    prompt: str = pydantic.Field(...)
    model: str = dalle_config.default_model
    size: str = dalle_config.default_size
    quality: str = dalle_config.default_quality
    n: int = dalle_config.default_n


__all__ = [
    "ImagesGenerateScheme",
]
