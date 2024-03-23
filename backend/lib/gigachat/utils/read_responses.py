import re
import typing


def get_image_id_from_response(response: typing.Mapping[str, typing.Any]) -> str | None:
    """Временная утилса.

    Пока GigachatArtClient не использует пидантик-схемы для полученных данных.
    """
    def find_uuid4(text: str) -> str | None:
        pattern = r'"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"'
        match = re.search(pattern, text)
        if match:
            return match.group(0)[1:-1]
        return None

    image_choices = response.get("choices")
    if not image_choices or len(image_choices) == 0:
        return None

    image_content = image_choices[0].get("message", {}).get("content")
    return find_uuid4(image_content)


__all__ = [
    "get_image_id_from_response",
]
