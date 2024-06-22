from typing import Any, AsyncGenerator
from abc import ABC, abstractmethod


class StorageProvider(ABC):

    @abstractmethod
    async def write(
        self,
        filename: str,
        tags: list[str],
        payload: AsyncGenerator[bytes, None],
    ) -> None:
        raise NotImplemented
