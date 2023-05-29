from sqlalchemy import Table, Column, String, Integer
from base.base_orm import BaseSqlORM, get_common_columns, get_common_id_column, get_id_fk_column
from base.base_dao import BaseDao
from entities.post import TikTokPostEntity


class TikTokPostORM(BaseSqlORM, TikTokPostEntity):
    __table__ = Table(
        "tiktok_post",
        BaseSqlORM.metadata,
        get_common_id_column(),
        Column("tiktok_id", String, nullable=False),
        Column("web_video_url", String, nullable=True),
        Column("digg_count", Integer, nullable=False),
        Column("share_count", Integer, nullable=False),
        Column("play_count", Integer, nullable=False),
        Column("comment_count", Integer, nullable=False),
        Column("tiktok_location", String, nullable=True),
        get_id_fk_column("author_id", "author.id"),
        get_id_fk_column("video_id", "video.id"),
        get_id_fk_column("music_id", "music.id"),
        *get_common_columns()
    )

class TikTokPostDAO(BaseDao):
    model = TikTokPostORM