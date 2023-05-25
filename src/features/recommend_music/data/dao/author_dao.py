from sqlalchemy import Table, Column, String
from base.base_orm import BaseSqlORM, get_common_columns, get_common_id_column
from base.base_dao import BaseDao
from entities.music import MusicEntity


class AuthorORM(BaseSqlORM, MusicEntity):
    __table__ = Table(
        "author",
        BaseSqlORM.metadata,
        get_common_id_column(),
        Column("name", String, nullable=False),
        Column("tiktok_id", String, nullable=True),
        Column("tiktok_nickname", String, nullable=True),
        Column("tiktok_display_name", String, nullable=True),
        Column("tiktok_signnature", String, nullable=True),
        Column("tiktok_avatar", String, nullable=True),
        Column("tiktok_is_private_account", String, nullable=True),
        Column("tiktok_is_verified", String, nullable=True),
        *get_common_columns()
    )

class AuthorDAO(BaseDao):
    model = AuthorORM