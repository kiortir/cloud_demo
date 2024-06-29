from pathlib import Path
from typing import Annotated, AsyncGenerator
from fastapi import APIRouter, File, UploadFile, Depends
from storage.providers.files import FilesStorageProvider
import repository.file
from schema.file import FileCreate
from db import AsyncConnection, get_connection

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
    f = FileCreate(name="test", hash="test", ext=".json", created_by=None)
    created_file = await repository.file.create_file(con, f)
    return created_file

## Написать методы для:
## Получения файла по id
## Изменение файла по id (имя/ext)
## Удаление файла по id
