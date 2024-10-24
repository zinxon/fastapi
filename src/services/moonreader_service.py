import re
from datetime import datetime
from fastapi import HTTPException
from typing import Optional

class MoonReaderService:
    def __init__(self, token: str, storage_service: any):
        self.token = f"Token {token}"
        self.storage = storage_service
        self.forbidden_chars_pattern = r'[<>:"/\\|?*]'  # Common forbidden filename characters

    def validate_token(self, auth_header: Optional[str]) -> bool:
        if not auth_header or auth_header != self.token:
            raise HTTPException(status_code=401, detail="Invalid authentication token")
        return True

    def format_highlight(self, highlight_data: dict) -> str:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        return (
            f"文: {highlight_data['text']}\n"
            f"批: {highlight_data.get('註', '')}\n"
            f"於: {current_time}\n\n---\n"
        )

    def create_yaml_header(self, title: str, author: str) -> str:
        return (
            f"---\n"
            f"title: {title}\n"
            f"author: {author}\n"
            f"---\n"
            f"書名: {title}\n"
            f"作者: {author}\n"
            f"簡介:\n"
            f"評價:\n\n---\n"
        )

    def get_file_path(self, title: str) -> str:
        safe_title = re.sub(self.forbidden_chars_pattern, "_", title)
        return f"支援類別檔案/MoonReader/{safe_title}.md"

    async def process_highlight(self, highlight_data: dict) -> bool:
        file_path = self.get_file_path(highlight_data['title'])
        highlight_text = self.format_highlight(highlight_data)

        if await self.storage.exists(file_path):
            await self.storage.append(file_path, highlight_text)
        else:
            yaml_header = self.create_yaml_header(
                highlight_data['title'],
                highlight_data['author']
            )
            await self.storage.append(file_path, yaml_header + highlight_text)

        return True