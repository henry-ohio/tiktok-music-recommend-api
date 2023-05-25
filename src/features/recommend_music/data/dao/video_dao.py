
from sqlalchemy import Table, Column, String, Float, Integer
from base.base_orm import BaseSqlORM, get_common_columns, get_common_id_column
from base.base_dao import BaseDao
from entities.video import VideoEntity


class VideoORM(BaseSqlORM, VideoEntity):
    __table__ = Table(
        "video",
        BaseSqlORM.metadata,
        get_common_id_column(),
        Column("original_download_address", String, nullable=False),
        Column("download_address", String, nullable=False),
        Column("format", String, nullable=True),
        Column("definition", String, nullable=True),
        Column("tiktok_cover", String, nullable=True),
        Column("tiktok_original_cover", String, nullable=True),
        Column("width", Integer, nullable=False),
        Column("height", Integer, nullable=False),
        Column("duration", Float, nullable=False),
        *get_common_columns()
    )

class VideoDAO(BaseDao):
    model = VideoORM
