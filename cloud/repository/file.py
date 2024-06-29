from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncConnection

from models.file import File
from schema.file import FileCreate, FileResponse

## Написать методы для:
## Получения файла по id
## Изменение файла по id (имя/ext)
## Удаление файла по id


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
