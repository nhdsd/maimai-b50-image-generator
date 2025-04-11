# pylint: disable = wildcard-import
"""maimaiDX B50生成器"""
import time
import datetime
import asyncio
import traceback
from typing import Optional

from libs import *

async def generate(
        username: Optional[str] = None,
        icon: Optional[str] = None,
        plate: Optional[str] = None
    ) -> str:
    """生成主函数"""
    mai_info = await get_user_info(username)
    draw_best = DrawBest(mai_info)

    try:
        pic = await draw_best.draw(icon, plate)
        path = OUTPUT + (datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.png')
        pic.save(path, "PNG")
    except Exception: # pylint: disable=broad-exception-caught
        return f"[FATAL]生成失败，Traceback如下\n{traceback.format_exc()}"
    return "[INFO]生成成功。"


if __name__ == '__main__':
    config = load_config()
    print('[INFO]开始生成B50...')
    result = asyncio.run(
        generate(**config)
    )
    print(result)
    print(f'[INFO]生成耗时{round(time.time() - START, 3)}秒。')
