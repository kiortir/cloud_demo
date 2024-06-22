from pathlib import Path
from typing import Annotated, AsyncGenerator
from fastapi import APIRouter, File, UploadFile, Depends
from storage.providers.files import FilesStorageProvider

router = APIRouter(prefix="/files")


@router.get("/")
def read_root():
    return {"Hello": "World"}


@router.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None, q2: str | None = None):
    return {"item_id": item_id, "q": q}


@router.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


async def as_generator(file: UploadFile) -> AsyncGenerator[bytes, None]:
    if not file.size:
        raise RuntimeError()
    chunk = 100
    total = 0
    while total < file.size:
        to_read = chunk if chunk + total < file.size else file.size - total
        yield await file.read(to_read)
        total += to_read


@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    print(file)
    provider = FilesStorageProvider(root_directory=Path("../"), media_base_url="http://localhost:8000/media/")
    url = await provider.write(
        file.filename or "test", ["demo", "join"], as_generator(file)
    )
    return {"filename": file.filename, "url": url}
