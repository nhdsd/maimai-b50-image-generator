"""配置文件读取"""
import os
import json
from typing import Dict, Optional, Union
from sys import exit as q

from .consts import user_config, Source

type Config = Optional[Union[str, int, bool]]

def load_config() -> Dict[str, Config]:
    """Load config from config.json."""
    if not os.path.exists(user_config):
        try:
            with open("user.txt", 'r', encoding='utf-8') as user:
                username = user.read()
            print('从user.txt读取用户名的API已经弃用，配置已经被转换为config.json。阅读changelog了解更多。')
        except FileNotFoundError:
            username = input('请输入Diving-Fish查分器网站用户名：')
        except Exception as e: # pylint: disable=broad-exception-caught
            print(f'读取user.txt失败，错误信息：{e}')
            q(1)
        with open(user_config,'w+',encoding='utf-8') as f:
            json.dump({'username': username}, f, ensure_ascii=False, indent=4)
    with open(user_config,'r',encoding='utf-8') as f:
        config = json.load(f)
    try:
        username = config['username']
    except KeyError:
        username = input('请输入Diving-Fish查分器网站用户名：')
        config['username'] = username
        with open(user_config,'w',encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
    try:
        icon = config['icon'] if config['icon'] != '' else None
    except KeyError:
        icon = None # pylint: disable=invalid-name
    try:
        plate = config['plate'] if config['plate'] != '' else None
    except KeyError:
        plate = None # pylint: disable=invalid-name
    try:
        plate_override = config['plate_override']
    except KeyError:
        plate_override = False
    try:
        local_first = config['local_first']
    except KeyError:
        local_first = False
    try:
        source = config['source']
        if source not in Source:
            print(f"[ERROR]配置文件错误，数据源不合法：{source}。请检查配置文件。已经切换为默认值 diving_fish。")
            source = "diving_fish"
    except KeyError:
        source = "diving_fish"

    return {
        'username': username,
        'icon': icon,
        'plate': plate,
        'plate_override': plate_override,
        'local_first': local_first,
        'source': source
    }
