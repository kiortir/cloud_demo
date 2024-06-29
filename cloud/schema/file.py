import datetime
from uuid import UUID
from pydantic import BaseModel


class FileBase(BaseModel):
    name: str
    ext: str
    hash: str
    created_by: UUID | None = None


class FileCreate(FileBase, BaseModel): ...


class FileResponse(FileBase, BaseModel):
    id: UUID
    created_at: datetime.datetime
