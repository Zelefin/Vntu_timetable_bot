from sqlalchemy import update, select
from sqlalchemy.dialects.postgresql import insert

from infrastructure.database.models import User
from infrastructure.database.repo.base import BaseRepo


class UserRepo(BaseRepo):
    async def get_or_create_user(
        self,
        user_id: int,
        full_name: str,
        username: str | None = None,
    ) -> User:
        """
        Creates or updates a new user in the database and returns the user object.
        :param user_id: The user's ID.
        :param full_name: The user's full name.
        :param username: The user's username. It's an optional parameter.
        :return: User object, None if there was an error while making a transaction.
        """

        insert_stmt = (
            insert(User)
            .values(
                user_id=user_id,
                username=username,
                full_name=full_name,
                active=True,
            )
            .on_conflict_do_update(
                index_elements=[User.user_id],
                set_=dict(
                    username=username,
                    full_name=full_name,
                    active=True,
                ),
            )
            .returning(User)
        )
        result = await self.session.execute(insert_stmt)

        await self.session.commit()
        return result.scalar_one()

    async def update_user_faculty_and_group(
        self,
        user_id: int,
        faculty_id: int,
        group_id: int,
        group_name: int,
        subgroup: int,
    ) -> User:
        """
        :param user_id: The user's ID.
        :param faculty_id: The user's faculty ID.
        :param group_id: The user's group ID.
        :param group_name: The user's group name.
        :param subgroup: The user's subgroup.
        :return: User object, None if there was an error while making a transaction.
        """
        update_stmt = (
            update(User)
            .where(User.user_id == user_id)
            .values(
                faculty_id=faculty_id,
                group_id=group_id,
                group_name=group_name,
                subgroup=subgroup,
            )
        ).returning(User)
        result = await self.session.execute(update_stmt)

        await self.session.commit()
        return result.scalar_one()

    async def all_users_ids(self) -> list[int]:
        return list(
            (
                await self.session.scalars(
                    select(User.user_id).where(User.active == True)
                )
            ).all()
        )

    async def inactive_user(self, user_id: int):
        update_stmt = update(User).where(User.user_id == user_id).values(active=False)
        await self.session.execute(update_stmt)
        await self.session.commit()
