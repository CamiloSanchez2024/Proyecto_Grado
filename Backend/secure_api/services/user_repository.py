from typing import Optional
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from secure_api.models.user import User


class UserRepository:
    """
    Data access layer for the User entity.
    All queries are async to avoid blocking the event loop.
    Pattern: Repository — isolates SQL from business logic.
    """

    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def find_by_username(self, username: str) -> Optional[User]:
        result = await self._db.execute(
            select(User).where(User.username == username.lower())
        )
        return result.scalar_one_or_none()

    async def find_by_email(self, email: str) -> Optional[User]:
        result = await self._db.execute(
            select(User).where(User.email == email.lower())
        )
        return result.scalar_one_or_none()

    async def find_by_id(self, user_id: str) -> Optional[User]:
        result = await self._db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def exists_username(self, username: str) -> bool:
        result = await self._db.execute(
            select(User.id).where(User.username == username.lower())
        )
        return result.scalar_one_or_none() is not None

    async def exists_email(self, email: str) -> bool:
        result = await self._db.execute(
            select(User.id).where(User.email == email.lower())
        )
        return result.scalar_one_or_none() is not None

    async def save(self, user: User) -> User:
        self._db.add(user)
        await self._db.flush()   # sends INSERT, gets generated values
        await self._db.refresh(user)  # reloads from DB (timestamps, etc.)
        return user

    async def update_last_login(self, user_id: str) -> None:
        await self._db.execute(
            update(User)
            .where(User.id == user_id)
            .values(last_login_at=datetime.now(timezone.utc))
        )

    async def update_password(self, user_id: str, new_hashed_password: str) -> None:
        await self._db.execute(
            update(User)
            .where(User.id == user_id)
            .values(
                hashed_password=new_hashed_password,
                updated_at=datetime.now(timezone.utc),
            )
        )

    async def list_all(self) -> list[User]:
        result = await self._db.execute(select(User).order_by(User.created_at.desc()))
        return list(result.scalars().all())
