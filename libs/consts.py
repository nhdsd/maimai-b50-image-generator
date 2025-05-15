"""常用常量"""
from pathlib import Path
import os
from typing import Dict
from enum import StrEnum, auto

# 文件路径
root: Path = Path(__file__).parent.parent
static: Path = root / 'static'
OUTPUT = './output/'
if not os.path.exists(OUTPUT):
    os.mkdir(OUTPUT)
user_config : Path = root / 'config.json'
config_json: Path = static / 'config.json'
music_file: Path = static / 'music_data.json'

# 静态资源路径
maimaidir: Path = static / 'mai' / 'pic'
coverdir: Path = static / 'mai' / 'cover'
customdir: Path = root / 'custom'
icondir: Path = static / 'mai' / 'icon'
platedir: Path = static / 'mai' / 'plate'

# 字体路径
HAN: Path = static / 'ResourceHanRoundedCN-Bold.ttf'
TORUS: Path = static / 'Torus SemiBold.otf'

# 常用变量
score_rank_l: Dict[str, str] = {'d': 'D', 'c': 'C', 'b': 'B', 'bb': 'BB', 'bbb': 'BBB', 'a': 'A',
                                'aa': 'AA','aaa': 'AAA', 's': 'S', 'sp': 'Sp', 'ss': 'SS',
                                'ssp': 'SSp', 'sss': 'SSS', 'sssp': 'SSSp'}
fcl: Dict[str, str] = {'fc': 'FC', 'fcp': 'FCp', 'ap': 'AP', 'app': 'APp'}
fsl: Dict[str, str] = {'fs': 'FS', 'fsp': 'FSp', 'fsd': 'FSD', 'fdx': 'FSD', 'fsdp': 'FSDp',
                       'fdxp': 'FSDp', 'sync': 'Sync'}

class Source(StrEnum):
    """数据源"""
    DIVING_FISH = auto()
    DIVING_FISH_LOCAL = auto()
