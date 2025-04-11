"""文件读写工具"""

import json
from typing import Any, Union
from pathlib import Path

import aiofiles

async def openfile(file: Path) -> Union[dict, list]:
    """异步IO读取文件"""
    async with aiofiles.open(file, 'r', encoding='utf-8') as f:
        data = json.loads(await f.read())
    return data


async def writefile(file: Path, data: Any) -> bool:
    """异步IO写入文件"""
    async with aiofiles.open(file, 'w', encoding='utf-8') as f:
        await f.write(json.dumps(data, ensure_ascii=False, indent=4))
    return True
