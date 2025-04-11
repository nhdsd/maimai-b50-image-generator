"""API"""

from io import BytesIO
from typing import List, Optional, Union, Any
import asyncio
import traceback
from pathlib import Path

from aiohttp import ClientSession, ClientTimeout
from .models import Music
from .consts import music_file, chart_file, coverdir
from .tools import openfile, writefile
from .errors import (
    UserNotFoundError, UserDisabledQueryError, ServerError, EnterError, CoverError, UnknownError
)

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
        print("正在与服务器通信...(获取游玩信息)")
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
    print("正在与服务器通信...(获取曲目信息)")
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
    print("正在与服务器通信...(获取谱面信息)")
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
