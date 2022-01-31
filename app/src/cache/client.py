from abc import ABC, abstractmethod
from typing import Any, Optional


class Abstract(ABC):
    def __init__(self, client: Any):
        self._client = client

    @property
    def client(self):
        return self._client

    @abstractmethod
    async def get(self, key: str) -> Optional[str]:
        pass

    @abstractmethod
    async def set(self, key: str, value: str, ttl: int) -> None:
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        pass


class Cache(Abstract):
    @property
    def client(self):
        return self._client

    async def get(self, key: str) -> Optional[str]:
        result = await self.client.get(key)
        return result

    async def set(self, key: str, value: str, ttl: int) -> None:
        await self.client.setex(key, ttl, value)

    async def delete(self, key: str) -> None:
        await self.client.delete(key)
