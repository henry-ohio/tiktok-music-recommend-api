from sqlalchemy import create_engine, orm
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine
from config.sql import SQLSettings
from kink import inject
from loguru import logger


@inject
def connect_database(db_settings: SQLSettings) -> AsyncEngine:
    logger.info(f'Connecting to SQL database at {db_settings.database_uri}')
    engine = create_async_engine(
        db_settings.database_uri, pool_pre_ping=True, future=True,
        echo=True,
    )

    return engine


@inject
async def create_database_tables(engine: AsyncEngine):
    from base.base_orm import BaseSqlORM
    async with engine.begin() as conn:
        await conn.run_sync(BaseSqlORM.metadata.create_all)


@inject
def get_async_session_builder(engine: AsyncEngine) -> orm.sessionmaker:
    print('creating session builder')
    factory = orm.sessionmaker(
        engine, class_=AsyncSession, autoflush=False, expire_on_commit=False,
    )
    return factory

@inject
def sync_session(db_settings: SQLSettings) -> orm.scoped_session:
    engine = create_engine(
        db_settings.database_uri, pool_pre_ping=True, future=True,
    )
    factory = orm.sessionmaker(
        engine, autoflush=False, expire_on_commit=False,
    )
    return orm.scoped_session(factory)
