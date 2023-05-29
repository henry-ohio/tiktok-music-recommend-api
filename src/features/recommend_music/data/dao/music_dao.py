
from sqlalchemy import Table, Column, String, Boolean, Integer
from base.base_orm import BaseSqlORM, get_common_columns, get_common_id_column, get_id_fk_column
from base.base_dao import BaseDao
from entities.music import MusicEntity, TiktokMusicEntity
from sqlalchemy.dialects.postgresql import UUID


class MusicORM(BaseSqlORM, MusicEntity):
    __table__ = Table(
        "music",
        BaseSqlORM.metadata,
        get_common_id_column(),
        Column("name", String, nullable=False),
        Column("author_name", String, nullable=True),
        Column("total_digg_count", Integer, nullable=True),
        Column("total_share_count", Integer, nullable=True),
        Column("total_play_count", Integer, nullable=True),
        Column("total_comment_count", Integer, nullable=True),
        *get_common_columns()
    )

class TiktokMusicORM(BaseSqlORM, TiktokMusicEntity):
    __table__ = Table(
        "tiktok_music",
        BaseSqlORM.metadata,
        get_common_id_column(),
        get_id_fk_column('music_id', 'music.id'),
        Column("tiktok_id", String, nullable=False, unique=True),
        Column("is_original", Boolean, default=True),
        Column("album", String, nullable=True),
        Column("play_url", String, nullable=False),
        Column("cover_medium_url", String, nullable=True),
        *get_common_columns()
    )

class MusicDAO(BaseDao):
    model = MusicORM

class TikTokMusicDAO(BaseDao):
    model = TiktokMusicORM