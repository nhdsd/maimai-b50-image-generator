"""
数据模型。
此文件需要进一步重构。
"""

from typing import Optional, List, Union
from collections import namedtuple

from pydantic import BaseModel, Field
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
