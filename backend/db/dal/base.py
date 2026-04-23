# backend/lib/db/base_crud.py

from typing import Generic, Optional, Sequence, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, select

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)


class AsyncPostgreSQLDAL(Generic[ModelType, CreateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, session: AsyncSession, id: str) -> Optional[ModelType]:
        return await session.get(self.model, id)

    async def list_all(self, session: AsyncSession) -> Sequence[ModelType]:
        result = await session.execute(select(self.model))
        return result.scalars().all()

    async def create(
        self,
        session: AsyncSession,
        obj_in: CreateSchemaType,
    ) -> ModelType:
        obj = self.model.model_validate(obj_in)  # converts Pydantic input to SQLModel
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    async def delete(self, session: AsyncSession, obj: ModelType) -> None:
        await session.delete(obj)
        await session.commit()
