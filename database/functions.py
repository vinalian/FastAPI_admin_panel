import datetime
from database.connector import get_session
from sqlalchemy import select, insert, delete, update
from database.models import User, Item
from database.basemodels import *
from typing import List, Dict

__all__ = [
    'get_all_users',
    'create_new_user',
    'remove_item',
    'edit_item',
    'add_new_item',
    'get_all_items',
    'get_user_by_username'
]


async def get_all_users() -> User:
    """
    Function select and return all users from database (table user).
    :return: Sqlalchemy object.
    """
    session = await get_session()
    result = await session.execute(select(User))
    await session.close()
    return result.scalars().all()


async def get_user_by_username(username: str) -> User:
    session = await get_session()
    result = await session.execute(select(User).where(User.login == username))
    await session.close()
    return result.scalars().one_or_none()


async def create_new_user(user_data: UserSchema) -> bool:
    session = await get_session()
    try:
        await session.execute(insert(User).values(
            login=user_data.login,
            hashed_password=user_data.hashed_password
        ))
        return True
    except:
        await session.rollback()
        return False
    finally:
        await session.commit()
        await session.close()


async def get_all_items() -> Item:
    session = await get_session()
    result = await session.execute(select(Item))
    await session.close()
    return result.scalars().all()


async def add_new_item(item_data: ItemSchema) -> bool:
    session = await get_session()
    try:
        await session.execute(insert(Item).values(
            name=item_data.name,
            user_id=int(item_data.user_id)
        ))
        return True
    except:
        await session.rollback()
        return False
    finally:
        await session.commit()
        await session.close()


async def remove_item(item_id: int) -> bool:
    session = await get_session()
    await session.execute(delete(Item).where(Item.id == item_id))
    await session.commit()
    await session.close()


async def edit_item(new_item_data: ItemSchema) -> bool:
    session = await get_session()
    await session.execute(update(Item).where(
        Item.id == int(new_item_data.id)
    ).values(
        name=new_item_data.name,
        user_id=int(new_item_data.user_id)
    ))
    await session.commit()
    await session.close()
