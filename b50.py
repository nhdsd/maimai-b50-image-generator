# pylint: disable = wildcard-import
"""maimaiDX B50生成器"""

import json
import time
import datetime
import os
import asyncio
import traceback
from typing import Optional

from libs import *

START = time.time()
mai_api = MaimaiAPI()

async def generate(
        username: Optional[str] = None,
        icon: Optional[str] = None,
        plate: Optional[str] = None
    ) -> str:
    """生成主函数"""
    obj = await mai_api.query_user(username)

    mai_info = UserInfo(**obj)
    draw_best = DrawBest(mai_info)

    try:
        pic = await draw_best.draw(icon, plate)
        path = OUTPUT + (datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.png')
        pic.save(path, "PNG")
    except Exception: # pylint: disable=broad-exception-caught
        return f"生成失败，Traceback如下\n{traceback.format_exc()}"
    return "生成成功"


if __name__ == '__main__':
    if not os.path.exists(user_config):
        try:
            with open("user.txt", 'r', encoding='utf-8') as user:
                c_username = user.read()
            print('从user.txt读取用户名的API已经弃用，配置已经被转换为config.json。阅读README了解更多。')
        except FileNotFoundError:
            c_username = input('请输入Diving-Fish查分器网站用户名：')
        finally:
            with open(user_config,'w+',encoding='utf-8') as config_f:
                json.dump({'username': c_username}, config_f, ensure_ascii=False, indent=4)
    with open(user_config,'r',encoding='utf-8') as config_f:
        config = json.load(config_f)
    try:
        c_username = config['username']
    except KeyError:
        c_username = input('请输入Diving-Fish查分器网站用户名：')
        config['username'] = c_username
        with open(user_config,'w',encoding='utf-8') as config_f:
            json.dump(config, config_f, ensure_ascii=False, indent=4)
    try:
        c_icon = config['icon']
    except KeyError:
        c_icon = None # pylint: disable=invalid-name
    try:
        c_plate = config['plate']
    except KeyError:
        c_plate = None # pylint: disable=invalid-name
    print('开始生成B50')
    result = asyncio.run(generate(username=c_username, icon=c_icon, plate = c_plate))
    print(result)
    print(f'生成耗时{round(time.time() - START, 3)}秒。')
