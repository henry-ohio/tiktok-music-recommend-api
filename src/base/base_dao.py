
import sqlalchemy as sa
from sqlalchemy import select, orm

from typing import (
    Dict,
    List,
    Union,
    Sequence,
    TypeVar,
)
from sqlalchemy.exc import NoResultFound
from sqlalchemy.sql.selectable import GenerativeSelect

from .base_orm import BaseSqlORM

from kink import di, inject
# Make sure the di is there
from modules.sql_database_module import get_async_session_builder
from loguru import logger
M = TypeVar('M', bound=BaseSqlORM)

di['session_builder'] = lambda di: get_async_session_builder()

class BaseDao:
    model: M

    @inject
    def __init__(self, session_builder) -> None:
        super().__init__()
        if self.model is None:
            raise Exception("This should be set to a Model class.")
        self.session_builder: orm.sessionmaker = session_builder

    def create(self, **attrs) -> M:
        return self.model(**attrs)

    def bulk_create(self, data) -> List[M]:
        objs = []
        for item in data:
            objs.append(self.model(**item))
        return objs

    def merge(self, instance: M, **attrs) -> M:
        for attr_key, attr_value in attrs.items():
            setattr(instance, attr_key, attr_value)
        return instance

    def has_pk(self, instance: M) -> bool:
        return bool([
            pk
            for pk in self.primary_keys
            if getattr(instance, pk.name) is not None
        ])

    def get_pk(self, instance: M) -> Union[Dict[str, M], M]:
        primary_keys = {}
        for pk in self.primary_keys:
            attr = getattr(instance, pk.name)
            if attr is not None:
                primary_keys[pk.name] = attr

        if len(primary_keys) > 1:
            return primary_keys

        return next(iter(primary_keys.values()))

    async def all(self, **attrs) -> List[M]:
        statement = sa.select(self.model).filter_by(**attrs)
        async with self.session_builder() as session:
            query_result = await session.execute(statement)
            return query_result.unique().scalars().all()

    async def find_in_by_pks(self, pks=None, *where, **attrs) -> M:
        statement = sa.select(self.model).where(*where).filter_by(**attrs)
        if pks is not None:
            async with self.session_builder() as session:
                localized_statement = statement.filter(
                    self.model.id.in_(pks)
                )
                query_result = await session.execute(localized_statement)
                results = query_result.unique().scalars().all()
                return results

        async with self.session_builder() as session:
            query_result = await session.execute(statement)
            results = query_result.unique().scalars().all()
        return results

    async def first(self, *where, **attrs) -> M:
        statement = sa.select(self.model).where(*where).filter_by(**attrs)
        async with self.session_builder() as session:
            query_result = await session.execute(statement)
            return query_result.first()

    async def find(self, accept_languages=None, *where, **attrs) -> M:
        statement = sa.select(self.model)\
            .where(*where)\
                .filter_by(**attrs)\
                .order_by()
        async with self.session_builder() as session:
            query_result = await session.execute(statement)
            results = query_result.unique().scalars().all()
        return results

    async def find_one(self, *where, **attrs) -> M:
        statement = sa.select(self.model).where(*where).filter_by(**attrs)
        async with self.session_builder() as session:
            query_result = await session.execute(statement)
            return query_result.unique().scalar()

    async def find_one_or_none(self, *where, **attrs) -> M:
        statement = sa.select(self.model).where(*where).filter_by(**attrs)
        async with self.session_builder() as session:
            query_result = await session.execute(statement)
            return query_result.unique().scalar_one_or_none()

    async def find_one_or_fail(self, *where, **attrs) -> M:
        instance = await self.find_one_or_none(*where, **attrs)
        if instance is None:
            raise NoResultFound('{0.__name__} not found'.format(self.model))

        return instance

    async def find_one_and_update(self, update_dict: dict, **where) -> M:
        instance = await self.find_one_or_fail(**where)
        if not instance:
            raise NoResultFound('{0.__name__} not found'.format(self.model))
        async with self.session_builder() as session:
            self.merge(instance, **update_dict)
            await session.commit()
            return instance

    async def delete(self, *where, **attrs) -> None:
        statement = sa.delete(self.model).where(*where).filter_by(**attrs)
        async with self.session_builder() as session:
            await session.execute(statement)
            await session.commit()
            return True

    # async def paginate(self , page , page_size , *where , **attrs) -> M :
    #     stmt = sa.select(self.model).

    async def delete(self, instance: M) -> None:
        async with self.session_builder() as session:
            await session.delete(instance)
            await session.commit()
            return True

    async def bulk_delete(self, instances: List[M]) -> None:
        async with self.session_builder() as session:
            for instance in instances:
                logger.info(f'Instance: {instance}')
                await session.delete(instance)
            await session.commit()
            return True

    async def get(self, id):
        async with self.session_builder() as session:
            instance = await session.get(self.model, id)
        return instance

    async def pre_save(self, instance: M) -> M:
        async with self.session_builder() as session:
            async with session.begin():
                session.add(instance)
            await session.flush()
        return instance

    async def save(self, instance: M) -> M:
        async with self.session_builder() as session:
            async with session.begin():
                session.add(instance)
            await session.flush()
            await session.commit()
        return instance

    async def bulk_save(self, instances: Sequence[M]) -> M:
        async with self.session_builder() as session:
            # await self.pre_bulk_save(instances)
            session.add_all(instances)
            await session.commit()
        return instances

    async def bulk_update(self, instances: List[M]) -> List[M]:
        async with self.session_builder() as session:
            session.add_all(instances)
            await session.flush()
            await session.commit()
        return instances

    async def get_by_ids(self, ids: tuple) -> Sequence[M]:
        async with self.session_builder() as session:
            return (await session.scalars(
                select(self.model).where(self.model.id.in_(ids))
            )).all()

    async def count(self, where: list = [], statement = None):
        select_model = statement if isinstance(statement, GenerativeSelect) else self.model
        count_statement = sa.select([sa.func.count()]).where(*where).select_from(select_model)
        async with self.session_builder() as session:
            return (await session.execute(count_statement)).scalar()
        