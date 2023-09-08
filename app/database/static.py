from models.models import Static
from database.database import (
    database_insert_one,
    database_update_one,
    database_delete_one,
)
from database.database import collections
from pydantic import ValidationError
from fastapi.exceptions import HTTPException


async def get_statc(title: str) -> Static:
    static_data = await collections["static"].find_one({"title": title})

    if not static_data:
        raise HTTPException(status_code=404, detail="Model data not found")

    try:
        return Static(**static_data)
    except ValidationError as error:
        raise HTTPException(status_code=400, detail=str(error))


async def create_static(static: Static) -> Static:
    try:
        result = await database_insert_one(collections["static"], static)
    except ValidationError as error:
        raise HTTPException(status_code=400, detail=str(error))

    return result


async def update_static(static: Static, static_id: str) -> Static:
    try:
        result = await database_update_one(static_id, static, collections["static"])
    except ValidationError as error:
        raise HTTPException(status_code=400, detail=str(error))

    return result


async def delete_static(static_id: str) -> None:
    try:
        result = await database_delete_one(static_id, collections["static"])
    except ValidationError as error:
        raise HTTPException(status_code=400, detail=str(error))

    return result
