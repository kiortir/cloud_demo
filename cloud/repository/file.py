from sqlalchemy import insert, select, update, delete, CursorResult
from sqlalchemy.ext.asyncio import AsyncConnection

from models.file import File
from schema.file import FileCreate, FileResponse

## Написать методы для:
## Получения файла по id
## Изменение файла по id (имя/ext)
## Удаление файла по id
async def get_file_to_id(connection: AsyncConnection, ind: int
) -> CursorResult:
    stmt = (
        select(File).where(File.id == ind)
    )

    return await connection.execute(stmt)

async def update_file_to_id(connection: AsyncConnection, ind: int,
                            value: dict):
    update_stmt = (
        update(File).where(File.id == ind)
        .values(
            value
        )
    )
    await connection.execute(update_stmt)
    await connection.commit()

async def delete_file_to_id(connection: AsyncConnection, ind: int
):
    stmt = (
        delete(File).where(File.id == ind)
    )
    await connection.execute(stmt)
    await connection.commit()

async def create_file(
    connection: AsyncConnection, file: FileCreate
) -> FileResponse:
    stmt = (
        insert(File)
        .values(
            name=file.name,
            ext=file.ext,
            hash=file.hash,
            created_by=file.created_by,
        )
        .returning(File)
    )
    file_rows = await connection.execute(stmt)
    await connection.commit()
    inserted_file = file_rows.first()
    if not inserted_file:
        raise RuntimeError()
    id, name, ext, hash, created_at, created_by = inserted_file
    return FileResponse(
        id=id,
        name=name,
        ext=ext,
        hash=hash,
        created_by=created_by,
        created_at=created_at,
    )
