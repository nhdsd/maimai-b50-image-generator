"""配置文件读取"""
import os
import json
from typing import Dict

from .consts import user_config
def load_config() -> Dict[str, str]:
    """读取配置文件"""
    if not os.path.exists(user_config):
        try:
            with open("user.txt", 'r', encoding='utf-8') as user:
                c_username = user.read()
            print('从user.txt读取用户名的API已经弃用，配置已经被转换为config.json。阅读changelog了解更多。')
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
    return {
        'username': c_username,
        'icon': c_icon,
        'plate': c_plate
    }
