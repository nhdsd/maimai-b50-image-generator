# pylint: disable = wildcard-import
"""maimaiDX B50生成器"""
import time
import datetime
import asyncio
import traceback
from sys import exit as q
from typing import cast

from libs import *

async def generate(config: dict[str, Config]) -> None:
    """Entry point for generating B50."""
    mai_info = await get_user_data(cast(str, config['source']), cast(str, config['username']))
    draw_best = DrawBest(mai_info)
    try:
        music_list = await music_list_dispatcher(cast(bool, config['local_first']))
    except KeyError:
        print(f"[FATAL]生成失败，Traceback如下\n{traceback.format_exc()}"
                "[INFO]请尝试关闭本地文件优先(local_first)选项。成功生成一次后可以考虑再次开启。")
        q(1)

    try:
        pic = await draw_best.draw(music_list, config)
        path = OUTPUT + (datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.png')
        pic.save(path, "PNG")
    except TypeError:
        print(f"[FATAL]生成失败，Traceback如下\n{traceback.format_exc()}"
                "[INFO]请尝试关闭本地文件优先(local_first)选项。成功生成一次后可以考虑再次开启。")
        q(1)
    except Exception: # pylint: disable=broad-exception-caught
        print(f"[FATAL]生成失败，Traceback如下\n{traceback.format_exc()}")
        q(1)
    print("[INFO]生成成功。")

if __name__ == '__main__':
    user_config = load_config()
    print('[INFO]开始生成B50...')
    asyncio.run(generate(user_config))
    print(f'[INFO]生成耗时{round(time.time() - START, 3)}秒。')
