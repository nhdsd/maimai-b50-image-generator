"""maimaiDX B50生成器"""

import json
import datetime
import os
import asyncio
import traceback
from io import BytesIO
from typing import Tuple, Dict, Any, List, Optional, Union
from collections import namedtuple

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from aiohttp import ClientSession, ClientTimeout
from pydantic import BaseModel, Field
import aiofiles

# maimaidx_error.py
class UserNotFoundError(Exception):
    """未找到玩家"""
    def __str__(self) -> str:
        return (
            '未找到此玩家，请确保此玩家的用户名和查分器中的用户名相同。'
            '如未绑定，请前往查分器官网进行绑定'
            'https://www.diving-fish.com/maimaidx/prober/'
        )


class UserDisabledQueryError(Exception):
    """玩家禁止查询"""
    def __str__(self) -> str:
        return '该用户禁止了其他人获取数据。'


class ServerError(Exception):
    """别名服务器内部错误"""
    def __str__(self) -> str:
        return '别名服务器错误，请联系插件开发者'


class EnterError(Exception):
    """参数错误"""
    def __str__(self) -> str:
        return '参数输入错误'


class CoverError(Exception):
    """图片错误"""


class UnknownError(Exception):
    """未知错误"""


# maimaidx_model.py
##### Music
class Stats(BaseModel):
    """统计信息"""
    cnt: Optional[float] = None
    diff: Optional[str] = None
    fit_diff: Optional[float] = None
    avg: Optional[float] = None
    avg_dx: Optional[float] = None
    std_dev: Optional[float] = None
    dist: Optional[List[int]] = None
    fc_dist: Optional[List[float]] = None


Notes1 = namedtuple('Notes', ['tap', 'hold', 'slide', 'brk'])
Notes2 = namedtuple('Notes', ['tap', 'hold', 'slide', 'touch', 'brk'])


class Chart(BaseModel):
    """谱面内容信息"""
    notes: Union[Notes1, Notes2]
    charter: str = None


class BasicInfo(BaseModel):
    """谱面基本信息"""
    title: str
    artist: str
    genre: str
    bpm: int
    release_date: Optional[str] = ''
    version: str = Field(alias='from')
    is_new: bool


class Music(BaseModel):
    """曲目信息"""
    id: str
    title: str
    type: str
    ds: List[float]
    level: List[str]
    cids: List[int]
    charts: List[Chart]
    basic_info: BasicInfo
    stats: Optional[List[Optional[Stats]]] = []
    diff: Optional[List[int]] = []


##### Best50
class ChartInfo(BaseModel):
    """谱面游玩信息"""
    achievements: float
    ds: float
    dxScore: int
    fc: Optional[str] = ''
    fs: Optional[str] = ''
    level: str
    level_index: int
    level_label: str
    ra: int
    rate: str
    song_id: int
    title: str
    type: str


class Data(BaseModel):
    """玩家游玩数据"""
    sd: Optional[List[ChartInfo]] = None
    dx: Optional[List[ChartInfo]] = None


class UserInfo(BaseModel):
    """玩家信息"""
    additional_rating: Optional[int]
    charts: Optional[Data]
    nickname: Optional[str]
    plate: Optional[str] = None
    rating: Optional[int]
    username: Optional[str]


##### PlayedInfo
class PlayInfo(BaseModel):
    """游玩信息"""
    achievements: float
    fc: str = ''
    fs: str = ''
    level: str
    level_index: int
    title: str
    type: str
    ds: float = 0
    dxScore: int = 0
    ra: int = 0
    rate: str = ''


class PlayInfoDefault(PlayInfo):
    """游玩信息默认值"""
    song_id: int = Field(alias='id')


class PlayInfoDev(PlayInfo):
    """游玩信息(内部值)"""
    level_label: str
    song_id: int


# tool.py

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

# 文件路径
root: Path = Path(__file__).parent
static: Path = root / 'static'
OUTPUT = './output/'
if not os.path.exists(OUTPUT):
    os.mkdir(OUTPUT)
config_json: Path = static / 'config.json'
music_file: Path = static / 'music_data.json'
chart_file: Path = static / 'music_chart.json'

# 静态资源路径
maimaidir: Path = static / 'mai' / 'pic'
coverdir: Path = static / 'mai' / 'cover'
platedir: Path = static / 'mai' / 'plate'

# 字体路径
MEIRYO: Path = static / 'ShangguMonoSC-Regular.otf'
SIYUAN: Path = static / 'ResourceHanRoundedCN-Bold.ttf'
TBFONT: Path = static / 'Torus SemiBold.otf'

# 常用变量
score_Rank_l: Dict[str, str] = {'d': 'D', 'c': 'C', 'b': 'B', 'bb': 'BB', 'bbb': 'BBB', 'a': 'A',
                                'aa': 'AA','aaa': 'AAA', 's': 'S', 'sp': 'Sp', 'ss': 'SS',
                                'ssp': 'SSp', 'sss': 'SSS', 'sssp': 'SSSp'}
fcl: Dict[str, str] = {'fc': 'FC', 'fcp': 'FCp', 'ap': 'AP', 'app': 'APp'}
fsl: Dict[str, str] = {'fs': 'FS', 'fsp': 'FSp', 'fsd': 'FSD', 'fdx': 'FSD', 'fsdp': 'FSDp',
                       'fdxp': 'FSDp', 'sync': 'Sync'}

# maimaidx_api_data.py
class MaimaiAPI:
    """API类"""
    MaiProxyAPI = 'https://www.diving-fish.com/api/maimaidxprober'
    MaiCover = 'https://www.diving-fish.com/covers'
    MaiAliasAPI = 'https://www.yuzuchan.moe/api/maimaidx'

    def __init__(self) -> None:
        return

    async def _request(self, method: str, url: str, **kwargs) -> Any:
        session = ClientSession(timeout=ClientTimeout(total=30))
        res = await session.request(method, url, **kwargs)

        data = None

        if self.MaiAliasAPI in url:
            if res.status == 200:
                data = (await res.json())['content']
            elif res.status == 400:
                raise EnterError
            elif res.status == 500:
                raise ServerError
            else:
                raise UnknownError
        elif self.MaiProxyAPI in url:
            if res.status == 200:
                data = await res.json()
            elif res.status == 400:
                raise UserNotFoundError
            elif res.status == 403:
                raise UserDisabledQueryError
            else:
                raise UnknownError
        await session.close()
        return data

    async def music_data(self):
        """获取曲目数据"""
        return await self._request('GET', self.MaiProxyAPI + '/music_data')

    async def chart_stats(self):
        """获取单曲数据"""
        return await self._request('GET', self.MaiProxyAPI + '/chart_stats')

    async def query_user(self, username: str):
        """
        请求用户数据

        - `project`: 查询的功能
            - `player`: 查询用户b50
            - `plate`: 按版本查询用户游玩成绩
        - `username`: 查分器用户名
        """
        post_data = {}
        post_data['username'] = username
        post_data['b50'] = True
        return await self._request('POST', self.MaiProxyAPI + '/query/player', json=post_data)

    async def transfer_music(self):
        """中转查分器曲目数据"""
        return await self._request('GET', self.MaiAliasAPI + '/maimaidxmusic')

    async def transfer_chart(self):
        """中转查分器单曲数据"""
        return await self._request('GET', self.MaiAliasAPI + '/maimaidxchartstats')

    async def download_music_pictrue(self, song_id: Union[int, str]) -> Union[Path, BytesIO]:
        """下载曲目封面"""
        try:
            if (file := coverdir / f'{song_id}.png').exists():
                return file
            song_id = int(song_id)
            if song_id > 100000:
                song_id -= 100000
                if (file := coverdir / f'{song_id}.png').exists():
                    return file
            if 1000 < song_id < 10000 or 10000 < song_id <= 11000:
                for _id in [song_id + 10000, song_id - 10000]:
                    if (file := coverdir / f'{_id}.png').exists():
                        return file
            pic = await self._request('GET', self.MaiCover + f'/{song_id:05d}.png')
            return BytesIO(pic)
        except CoverError:
            return coverdir / '11000.png'
        except Exception: # pylint: disable=broad-exception-caught
            return coverdir / '11000.png'

maiApi = MaimaiAPI()


# maimaidx_music.py
class MusicList(List[Music]):
    """曲目列表类"""
    def by_id(self, music_id: Union[str, int]) -> Optional[Music]:
        """按ID搜索"""
        for music in self:
            if music.id == str(music_id):
                return music
        return None


async def get_music_list() -> MusicList:
    """获取所有数据"""
    # MusicData
    try:
        try:
            music_data = await maiApi.music_data()
            await writefile(music_file, music_data)
        except asyncio.exceptions.TimeoutError:
            print('从diving-fish获取maimaiDX曲目数据超时，正在使用yuzuapi中转获取曲目数据')
            music_data = await maiApi.transfer_music()
            await writefile(music_file, music_data)
        except UnknownError:
            print('从diving-fish获取maimaiDX曲目数据失败，请检查网络环境。已切换至本地暂存文件')
            music_data = await openfile(music_file)
        except Exception: # pylint: disable=broad-exception-caught
            print(f'Error: {traceback.format_exc()}')
            print('maimaiDX曲目数据获取失败，请检查网络环境。已切换至本地暂存文件')
            music_data = await openfile(music_file)
    except FileNotFoundError:
        print(
            '未找到文件，请自行使用浏览器访问 "https://www.diving-fish.com/api/maimaidxprober/music_data" '
            '将内容保存为 "music_data.json" 存放在 "static" 目录下并重启此工具'
        )
        raise
    # ChartStats
    try:
        try:
            chart_stats = await maiApi.chart_stats()
            await writefile(chart_file, chart_stats)
        except asyncio.exceptions.TimeoutError:
            print('从diving-fish获取maimaiDX数据获取超时，正在使用yuzuapi中转获取单曲数据')
            chart_stats = await maiApi.transfer_chart()
            await writefile(chart_file, chart_stats)
        except UnknownError:
            print('从diving-fish获取maimaiDX单曲数据获取错误。已切换至本地暂存文件')
            chart_stats = await openfile(chart_file)
        except Exception: # pylint: disable=broad-exception-caught
            print(f'Error: {traceback.format_exc()}')
            print('maimaiDX数据获取错误，请检查网络环境。已切换至本地暂存文件')
            chart_stats = await openfile(chart_file)
    except FileNotFoundError:
        print(
            '未找到文件，请自行使用浏览器访问 "https://www.diving-fish.com/api/maimaidxprober/chart_stats" '
            '将内容保存为 "chart_stats.json" 存放在 "static" 目录下并重启此工具'
        )
        raise

    total_list: MusicList = MusicList()
    for music in music_data:
        if music['id'] in chart_stats['charts']:
            _stats = [_data if _data else None for _data in chart_stats['charts'][music['id']]] \
                if {} in chart_stats['charts'][music['id']] else chart_stats['charts'][music['id']]
        else:
            _stats = None
        total_list.append(Music(stats=_stats, **music))

    return total_list

music_list = asyncio.run(get_music_list())

# image.py
# pylint: disable-next=too-few-public-methods
class DrawText:
    """文字绘制类"""
    def __init__(self, image: ImageDraw.ImageDraw, font: Path) -> None:
        self._img = image
        self._font = str(font)

    #pylint: disable-next=too-many-arguments, too-many-positional-arguments
    def draw(self,
             pos_x: int,
             pos_y: int,
             size: int,
             text: Union[str, int, float],
             color: Tuple[int, int, int, int] = (255, 255, 255, 255),
             anchor: str = 'lt',
             stroke_width: int = 0,
             stroke_fill: Tuple[int, int, int, int] = (0, 0, 0, 0),
             multiline: bool = False):
        """绘图主方法"""
        font = ImageFont.truetype(self._font, size)
        if multiline:
            self._img.multiline_text(
                (pos_x, pos_y),
                str(text),
                color,
                font,
                anchor,
                stroke_width=stroke_width,
                stroke_fill=stroke_fill
            )
        else:
            self._img.text(
                (pos_x, pos_y),
                str(text),
                color,
                font,
                anchor,
                stroke_width=stroke_width,
                stroke_fill=stroke_fill
            )


def music_picture(music_id: Union[int, str]) -> Path:
    """
    获取谱面图片路径

    Params:
        `music_id`: 谱面 ID
    Returns:
        `Path`
    """
    music_id = int(music_id)
    if (_path := coverdir / f'{music_id}.png').exists():
        return _path
    if music_id > 100000:
        music_id -= 100000
        if (_path := coverdir / f'{music_id}.png').exists():
            return _path
    if 1000 < music_id < 10000 or 10000 < music_id <= 11000:
        for _id in [music_id + 10000, music_id - 10000]:
            if (_path := coverdir / f'{_id}.png').exists():
                return _path
    return coverdir / '11000.png'

# maimai_best_50.py
# pylint: disable-next=too-few-public-methods
class ScoreBaseImage:
    """基本分数绘制类"""
    _diff = [
        Image.open(maimaidir / 'b50_score_basic.png'),
        Image.open(maimaidir / 'b50_score_advanced.png'),
        Image.open(maimaidir / 'b50_score_expert.png'),
        Image.open(maimaidir / 'b50_score_master.png'),
        Image.open(maimaidir / 'b50_score_remaster.png')
    ]
    _rise = [
        Image.open(maimaidir / 'rise_score_basic.png'),
        Image.open(maimaidir / 'rise_score_advanced.png'),
        Image.open(maimaidir / 'rise_score_expert.png'),
        Image.open(maimaidir / 'rise_score_master.png'),
        Image.open(maimaidir / 'rise_score_remaster.png')
    ]
    text_color = (124, 129, 255, 255)
    t_color = [
        (255, 255, 255, 255),
        (255, 255, 255, 255),
        (255, 255, 255, 255),
        (255, 255, 255, 255),
        (138, 0, 226, 255)
    ]
    id_color = [
        (129, 217, 85, 255),
        (245, 189, 21, 255),
        (255, 129, 141, 255),
        (159, 81, 220, 255),
        (138, 0, 226, 255)
    ]
    bg_color = [
        (111, 212, 61, 255),
        (248, 183, 9, 255),
        (255, 129, 141, 255),
        (159, 81, 220, 255),
        (219, 170, 255, 255)
    ]
    id_diff = [Image.new('RGBA', (55, 10), color) for color in bg_color]

    title_bg = Image.open(maimaidir / 'title.png')
    title_lengthen_bg = Image.open(maimaidir / 'title-lengthen.png')
    design_bg = Image.open(maimaidir / 'design.png')
    aurora_bg = Image.open(maimaidir / 'aurora.png').convert('RGBA').resize((1400, 220))
    shines_bg = Image.open(maimaidir / 'bg_shines.png').convert('RGBA')
    pattern_bg = Image.open(maimaidir / 'pattern.png')
    rainbow_bg = Image.open(maimaidir / 'rainbow.png').convert('RGBA')
    rainbow_bottom_bg = Image.open(
        maimaidir / 'rainbow_bottom.png'
    ).convert('RGBA').resize((1200, 200))

    def __init__(self, image: Image.Image = None) -> None:
        self._im = image
        dr = ImageDraw.Draw(self._im)
        self._sy = DrawText(dr, SIYUAN)
        self._tb = DrawText(dr, TBFONT)

    #pylint: disable-next=too-many-locals
    def whiledraw(
        self,
        data: Union[List[ChartInfo], List[PlayInfoDefault], List[PlayInfoDev]],
        best: bool,
        height: int = 0
    ) -> None:
        """
        循环绘制成绩

        Params:
            `data`: 数据
            `dx`: 是否为新版本成绩
            `height`: 起始高度
        """
        # y为第一排纵向坐标，dy为各行间距
        dy = 114
        if data and isinstance(data[0], ChartInfo):
            y = 235 if best else 1085
        else:
            y = height
        for num, info in enumerate(data):
            if num % 5 == 0:
                x = 16
                y += dy if num != 0 else 0
            else:
                x += 276

            cover = Image.open(music_picture(info.song_id)).resize((75, 75))
            version = Image.open(maimaidir / f'{info.type.upper()}.png').resize((37, 14))
            if info.rate.islower():
                rate = Image.open(
                    maimaidir / f'UI_TTR_Rank_{score_Rank_l[info.rate]}.png'
                ).resize((63, 28))
            else:
                rate = Image.open(maimaidir / f'UI_TTR_Rank_{info.rate}.png').resize((63, 28))

            self._im.alpha_composite(self._diff[info.level_index], (x, y))
            self._im.alpha_composite(cover, (x + 12, y + 12))
            self._im.alpha_composite(version, (x + 51, y + 91))
            self._im.alpha_composite(rate, (x + 92, y + 78))
            if info.fc:
                fc = Image.open(
                    maimaidir / f'UI_MSS_MBase_Icon_{fcl[info.fc]}.png'
                ).resize((34, 34))
                self._im.alpha_composite(fc, (x + 154, y + 77))
            if info.fs:
                fs = Image.open(
                    maimaidir / f'UI_MSS_MBase_Icon_{fsl[info.fs]}.png'
                ).resize((34, 34))
                self._im.alpha_composite(fs, (x + 185, y + 77))

            dxscore = sum(music_list.by_id(str(info.song_id)).charts[info.level_index].notes) * 3
            dxnum = dx_score(info.dxScore / dxscore * 100)
            if dxnum:
                self._im.alpha_composite(
                    Image.open(
                        maimaidir / f'UI_GAM_Gauge_DXScoreIcon_0{dxnum}.png'
                    ).resize((47, 26)),
                    (x + 217, y + 80)
                )

            self._tb.draw(
                x + 26,
                y + 98,
                13,
                info.song_id,
                self.id_color[info.level_index],
                anchor='mm'
            )
            title = info.title
            if coloum_width(title) > 18:
                title = change_column_width(title, 17) + '...'
            self._sy.draw(
                x + 93,
                y + 14,
                14,
                title,
                self.t_color[info.level_index],
                anchor='lm'
            )
            self._tb.draw(
                x + 93,
                y + 38,
                30,
                f'{info.achievements:.4f}%', self.t_color[info.level_index],
                anchor='lm'
            )
            self._tb.draw(
                x + 219,
                y + 65,
                15,
                f'{info.dxScore}/{dxscore}',
                self.t_color[info.level_index],
                anchor='mm'
            )
            self._tb.draw(
                x + 93,
                y + 65,
                15,
                f'{info.ds} -> {info.ra}',
                self.t_color[info.level_index],
                anchor='lm'
            )


class DrawBest(ScoreBaseImage):
    """B50 绘制类"""
    def __init__(self, user_info: UserInfo) -> None:
        super().__init__(Image.open(maimaidir / 'b50_bg.png').convert('RGBA'))
        self.user_name = user_info.nickname
        self.plate = user_info.plate
        self.add_rating = user_info.additional_rating
        self.rating = user_info.rating
        self.sd_best = user_info.charts.sd
        self.dx_best = user_info.charts.dx

    def _find_rating_picture(self) -> str:
        """
        寻找指定的Rating图片

        Returns:
            `str` 返回图片名称
        """
        if self.rating < 1000:
            num = '01'
        elif self.rating < 2000:
            num = '02'
        elif self.rating < 4000:
            num = '03'
        elif self.rating < 7000:
            num = '04'
        elif self.rating < 10000:
            num = '05'
        elif self.rating < 12000:
            num = '06'
        elif self.rating < 13000:
            num = '07'
        elif self.rating < 14000:
            num = '08'
        elif self.rating < 14500:
            num = '09'
        elif self.rating < 15000:
            num = '10'
        else:
            num = '11'
        return f'UI_CMN_DXRating_{num}.png'

    def _find_match_level_picture(self) -> str:
        """
        寻找匹配等级图片

        Returns:
            `str` 返回图片名称
        """
        if self.add_rating <= 10:
            num = f'{self.add_rating:02d}'
        else:
            num = f'{self.add_rating + 1:02d}'
        return f'UI_DNM_DaniPlate_{num}.png'

    async def draw(self) -> Image.Image:
        """异步绘制"""
        logo = Image.open(maimaidir / 'logo.png').resize((249, 120))
        dx_rating = Image.open(maimaidir / self._find_rating_picture()).resize((186, 35))
        name = Image.open(maimaidir / 'Name.png')
        match_level = Image.open(maimaidir / self._find_match_level_picture()).resize((80, 32))
        class_level = Image.open(maimaidir / 'UI_FBR_Class_00.png').resize((90, 54))
        rating = Image.open(maimaidir / 'UI_CMN_Shougou_Rainbow.png').resize((270, 27))

        self._im.alpha_composite(logo, (14, 60))
        if self.plate:
            plate = Image.open(platedir / f'{self.plate}.png').resize((800, 130))
        else:
            plate = Image.open(maimaidir / 'UI_Plate_300501.png').resize((800, 130))
        self._im.alpha_composite(plate, (300, 60))
        icon = Image.open(maimaidir / 'UI_Icon_309503.png').resize((120, 120))
        self._im.alpha_composite(icon, (305, 65))
        self._im.alpha_composite(dx_rating, (435, 72))
        rating_value = f'{self.rating:05d}'
        for n, i in enumerate(rating_value):
            self._im.alpha_composite(
                Image.open(maimaidir / f'UI_NUM_Drating_{i}.png').resize((17, 20)),
                (520 + 15 * n, 80)
            )
        self._im.alpha_composite(name, (435, 115))
        self._im.alpha_composite(match_level, (625, 120))
        self._im.alpha_composite(class_level, (620, 60))
        self._im.alpha_composite(rating, (435, 160))

        self._sy.draw(445, 135, 25, self.user_name, (0, 0, 0, 255), 'lm')
        sdrating, dxrating = sum((_.ra for _ in self.sd_best)), sum((_.ra for _ in self.dx_best))
        self._tb.draw(
            570, 172, 17,
            f'B35: {sdrating} + B15: {dxrating} = {self.rating}',
            (0, 0, 0, 255), 'mm', 3, (255, 255, 255, 255)
        )
        self._sy.draw(
            700, 1570, 27,
            'Designed by Yuri-YuzuChaN & BlueDeer233.',
            self.text_color, 'mm', 5, (255, 255, 255, 255)
        )

        self.whiledraw(self.sd_best, True)
        self.whiledraw(self.dx_best, False)

        return self._im


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


async def generate(username: Optional[str] = None) -> str:
    """生成主函数"""
    obj = await maiApi.query_user(username)

    mai_info = UserInfo(**obj)
    draw_best = DrawBest(mai_info)

    try:
        pic = await draw_best.draw()
        path = OUTPUT + (datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.png')
        pic.save(path, "PNG")
    except Exception: # pylint: disable=broad-exception-caught
        return f"生成失败，Traceback如下\n{traceback.format_exc()}"
    return "生成成功"


if __name__ == '__main__':
    user_path : Path = root / 'user.txt'
    if not os.path.exists(user_path):
        target_username = input('请输入Diving-Fish查分器网站用户名：')
        with open(user_path,'w+',encoding='utf-8') as user:
            user.write(target_username)
    with open(user_path,'r',encoding='utf-8') as user:
        target_username = user.read()
    print('开始生成B50')
    result = asyncio.run(generate(username=target_username))
    print(result)
