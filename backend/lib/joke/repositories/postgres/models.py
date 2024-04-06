import uuid

import sqlalchemy

import lib.utils.sqlalchemy as sqlalchemy_utils


class Joke(sqlalchemy_utils.Base):
    __tablename__ = "jokes"

    joke_id = sqlalchemy_utils.mapped_column(
        mapped_type=uuid.UUID,
        column_name="joke_id",
        column_type=sqlalchemy.UUID,
        primary_key=True,
        default=uuid.uuid4,
    )
    text_final = sqlalchemy_utils.mapped_column(
        mapped_type=str,
        column_name="text_final",
        column_type=sqlalchemy.String,
    )
    image_id = sqlalchemy_utils.mapped_column(
        mapped_type=str,
        column_name="image_id",
        column_type=sqlalchemy.String,
    )


__all__ = [
    "Joke",
]
