from pathlib import Path
from typing import Annotated, AsyncGenerator
from fastapi import APIRouter, File, UploadFile, Depends
from storage.providers.files import FilesStorageProvider
import repository.file
from schema.file import FileCreate
from db import AsyncConnection, get_connection

from repository.file import get_file_to_id, update_file_to_id, delete_file_to_id

router = APIRouter(prefix="/files")


async def as_generator(file: UploadFile) -> AsyncGenerator[bytes, None]:
    if not file.size:
        raise RuntimeError()
    chunk = 100
    total = 0
    while total < file.size:
        to_read = chunk if chunk + total < file.size else file.size - total
        yield await file.read(to_read)
        total += to_read

async def get_ext_from_file(file: UploadFile) -> str:
    if file.filename != None:
        ext: str = '.' + '.'.join(file.filename.split('.')[1:])
    return ext

async def get_name_from_file(file: UploadFile) -> str:
    if file.filename != None:
        name: str = file.filename.split('.')[0]
    return name

## TODO Начать прокидывать имя файла и ext из запроса
@router.post("/upload/")
async def create_upload_file(
    file: UploadFile, con: AsyncConnection = Depends(get_connection)
):
    # print(file)
    # provider = FilesStorageProvider(root_directory=Path("../"), media_base_url="http://localhost:8000/media/")
    # url = await provider.write(
    #     file.filename or "test", ["demo", "join"], as_generator(file)
    # )
    # return {"filename": file.filename, "url": url}
    name = await get_name_from_file(file)
    ext = await get_ext_from_file(file)
    f = FileCreate(name=name, hash="test", ext=ext, created_by=None)
    created_file = await repository.file.create_file(con, f)
    return created_file

@router.get("/{id}")
async def get_upload_file_from_id(id: int, con: AsyncConnection = Depends(get_connection)
):
    return await get_file_to_id(con, id)

@router.patch("/{id}")
async def update_upload_file_from_id(id: int, value: dict, con: AsyncConnection = Depends(get_connection)
):
    return await update_file_to_id(con, id, value)

@router.delete("/{id}")
async def delete_upload_file_from_id(id: int, con: AsyncConnection = Depends(get_connection)
):
    return await delete_file_to_id(con, id)

## Написать методы для:
## Получения файла по id
## Изменение файла по id (имя/ext)
## Удаление файла по id
