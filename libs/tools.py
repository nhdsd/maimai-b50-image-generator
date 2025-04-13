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

def dx_score(dx: int) -> int:
    """
    获取DX评分星星数量

    Params:
        `dx`: dx百分比
    Returns:
        `int` 返回星星数量
    """
    if dx <= 85:
        star_count = 0
    elif dx <= 90:
        star_count = 1
    elif dx <= 93:
        star_count = 2
    elif dx <= 95:
        star_count = 3
    elif dx <= 97:
        star_count = 4
    else:
        star_count = 5
    return star_count


def get_char_width(o: int) -> int:
    """字符宽度"""
    widths = [
        (126, 1), (159, 0), (687, 1), (710, 0), (711, 1), (727, 0), (733, 1), (879, 0), (1154, 1),
        (1161, 0), (4347, 1), (4447, 2), (7467, 1), (7521, 0), (8369, 1), (8426, 0), (9000, 1),
        (9002, 2), (11021, 1), (12350, 2), (12351, 1), (12438, 2), (12442, 0), (19893, 2),
        (19967, 1), (55203, 2), (63743, 1), (64106, 2), (65039, 1), (65059, 0), (65131, 2),
        (65279, 1), (65376, 2), (65500, 1), (65510, 2), (120831, 1), (262141, 2), (1114109, 1)
    ]
    if o in {0xe, 0xf}:
        return 0
    for num, wid in widths:
        if o <= num:
            return wid
    return 1


def coloum_width(s: str) -> int:
    """列宽"""
    res = 0
    for ch in s:
        res += get_char_width(ord(ch))
    return res


def change_column_width(s: str, length: int) -> str:
    """调整列宽"""
    res = 0
    s_list = []
    for ch in s:
        res += get_char_width(ord(ch))
        if res <= length:
            s_list.append(ch)
    return ''.join(s_list)


def plate_finder(name: str) -> int:
    """将汉字牌子名转化为数字编号"""
    if name == "霸者":
        return 6148
    if name[0] == "真":
        return 6101 + ("極", "神", "舞舞").index(name[1:])
    gen_mapping = {
        "超": 6104, "檄": 6108, "橙": 6112, "暁": 6116, "桃": 6120, "櫻": 6124,
        "紫": 6128, "堇": 6132, "白": 6136, "雪": 6140, "辉": 6144, "舞": 6149,
        "熊": 55101, "爽": 159101, "宙": 259101, "祭": 359101, "双": 459101, "宴": 559101,
    }
    try:
        gen = gen_mapping[name[0]]
    except KeyError:
        raise ValueError(f"[FATAL]无法识别的牌子：{name}") from None
    level = ("極", "将", "神", "舞舞").index(name[1:])
    if level == -1:
        raise ValueError(f"[FATAL]无法识别的牌子：{name}") from None
    return gen + level
