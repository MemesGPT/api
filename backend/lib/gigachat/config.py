import pydantic


class GigachatConfig(pydantic.BaseSettings):
    """Конфиги для Гигачата.

    TODO: возможно лучше будут смотреться в настройках приложения
    """

    auth_url: str = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    chat_completions_url: str = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    fetch_img_by_id_url: str = "https://gigachat.devices.sberbank.ru/api/v1/files/{}/content"
    start_art_promt_template: str = "Нарисуй {}"

    default_model: str = "GigaChat:latest"
    default_temperature:  float = 0.7
    default_top_p: float = 0.1
    default_n: int = 1
    default_stream: bool = False
    default_max_tokens: int = 1000
    default_repetition_penalty: int = 1
    default_update_interval: int = 0
