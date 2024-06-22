from uuid import uuid4
from pathlib import Path
from typing import AsyncGenerator

import aiofiles
from ..abstract import StorageProvider


class FilesStorageProvider(StorageProvider):
    def __init__(self, root_directory: Path, media_base_url: str) -> None:
        self.root_directory = root_directory
        self.media_base_url = media_base_url

    async def write(
        self,
        filename: str,
        tags: list[str],
        payload: AsyncGenerator[bytes, None],
    ) -> str:
        # TODO: aiofiles (асихнронность)
        subfolders = Path("/".join(tags))
        path = self.root_directory / subfolders
        path.mkdir(parents=True, exist_ok=True)
        filename_with_hash = f"{uuid4()}_{filename}"
        filepath = path / filename_with_hash
        async with aiofiles.open(filepath, "wb+") as object_file:
            async for chunk in payload:
                await object_file.write(chunk)
        return self.media_base_url + str(subfolders / filename_with_hash)
