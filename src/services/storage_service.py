from typing import Optional

class StorageService:
    async def exists(self, path: str) -> bool:
        # Implement your storage check logic here
        pass

    async def append(self, path: str, content: str) -> bool:
        # Implement your storage append logic here
        pass