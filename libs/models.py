"""
数据模型。
此文件需要进一步重构。
"""

from typing import Optional, List, Union, NamedTuple

from pydantic import BaseModel, Field

Notes1 = NamedTuple('Notes', [('tap', int), ('hold', int), ('slide', int), ('brk', int)])
Notes2 = NamedTuple(
    'Notes',
    [('tap', int), ('hold', int), ('slide', int), ('touch', int), ('brk', int)]
)


class Chart(BaseModel):
    """Chart Info"""
    notes: Union[Notes1, Notes2]
    charter: Optional[str] = None


class BasicInfo(BaseModel):
    """Chart Basic Info"""
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
    sd: List[ChartInfo]
    dx: List[ChartInfo]


class UserInfo(BaseModel):
    """玩家信息"""
    additional_rating: int
    charts: Data
    nickname: str
    plate: Optional[str] = None
    rating: int
    username: str
