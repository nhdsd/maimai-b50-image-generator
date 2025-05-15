"""
API interface for diving fish.
"""

from io import BytesIO
from typing import List, Dict, Union, Any, cast
import asyncio
import traceback
from pathlib import Path
from aiohttp import ClientSession, ClientTimeout
from .models import Music, UserInfo
from .consts import music_file, coverdir
from .tools import openfile, writefile
from .errors import (
    UserNotFoundError, UserDisabledQueryError, ServerError, EnterError, CoverError, UnknownError
)

MAI_PROXY_API = 'https://www.diving-fish.com/api/maimaidxprober'
MAI_COVER = 'https://www.diving-fish.com/covers'
MAI_ALIAS_API = 'https://www.yuzuchan.moe/api/maimaidx'

class MaimaiAPI:
    """
    API Class
    """

    async def _request(self, method: str, url: str, **kwargs: Any) -> Any:
        session = ClientSession(timeout=ClientTimeout(total=30))
        res = await session.request(method, url, **kwargs)

        data = None

        if MAI_ALIAS_API in url:
            if res.status == 200:
                data = (await res.json())['content']
            elif res.status == 400:
                raise EnterError
            elif res.status == 500:
                raise ServerError
            else:
                raise UnknownError
        elif MAI_PROXY_API in url:
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

    async def music_data(self) -> List[Dict[str, Any]]:
        """Get music data from diving fish."""
        return await self._request('GET', MAI_PROXY_API + '/music_data')

    async def query_user(self, username: str) -> Dict[str, Any]:
        """Get user data from diving fish."""
        post_data = {}
        post_data['username'] = username
        post_data['b50'] = True
        print("[INFO]正在与服务器通信...(获取游玩信息)")
        return await self._request('POST', MAI_PROXY_API + '/query/player', json=post_data)

    async def transfer_music(self) -> List[Dict[str, Any]]:
        """Get music data from yuzuapi."""
        return await self._request('GET', MAI_ALIAS_API + '/maimaidxmusic')

    async def download_music_pictrue(self, song_id: Union[int, str]) -> Union[Path, BytesIO]:
        """Download music illustration from diving fish."""
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
            pic = await self._request('GET', MAI_COVER + f'/{song_id:05d}.png')
            return BytesIO(pic)
        except CoverError:
            return coverdir / '11000.png'
        except Exception: # pylint: disable=broad-exception-caught
            return coverdir / '11000.png'

mai_api = MaimaiAPI()

class MusicList(List[Music]):
    """Music List"""
    def by_id(self, music_id: Union[str, int]) -> Music:
        """Search music by id"""
        for music in self:
            if music.id == str(music_id):
                return music
        raise ValueError(f"[FATAL]曲目ID {music_id} 不存在")


async def get_music_list() -> MusicList:
    """Get all music data from diving fish."""
    print("[INFO]正在与服务器通信...(获取曲目信息)")
    try:
        try:
            music_data = await mai_api.music_data()
            await writefile(music_file, music_data)
        except asyncio.exceptions.TimeoutError:
            print('[ERROR]从diving-fish获取maimaiDX曲目数据超时，正在使用yuzuapi中转获取曲目数据')
            music_data = await mai_api.transfer_music()
            await writefile(music_file, music_data)
        except UnknownError:
            print('[ERROE]从diving-fish获取maimaiDX曲目数据失败，请检查网络环境。已切换至本地暂存文件')
            music_data = cast(List[Dict[str, Any]], await openfile(music_file))
        except Exception: # pylint: disable=broad-exception-caught
            print(f'[ERROR]Error: {traceback.format_exc()}')
            print('[ERROR]maimaiDX曲目数据获取失败，请检查网络环境。已切换至本地暂存文件')
            music_data = cast(List[Dict[str, Any]], await openfile(music_file))
    except FileNotFoundError:
        print(
            '[FATAL]未找到文件，请自行使用浏览器访问 "https://www.diving-fish.com/api/maimaidxprober/music_data" '
            '将内容保存为 "music_data.json" 存放在 "static" 目录下并重启此工具'
        )
        raise

    print("[INFO]正在与服务器通信...(获取谱面信息)")

    total_list: MusicList = MusicList((Music(**music) for music in music_data))

    return total_list

async def get_local_music_list() -> MusicList:
    """Get all music data from local file."""
    print("[INFO]正在读取本地曲目数据...")
    try:
        music_data = cast(List[Dict[str, Any]], await openfile(music_file))
    except FileNotFoundError:
        print(
            '[ERROR]未找到文件，即将向服务器请求曲目信息。\n'
            '[INFO]正在与服务器通信...(获取曲目信息)'
        )
        try:
            music_data = await mai_api.music_data()
            await writefile(music_file, music_data)
        except asyncio.exceptions.TimeoutError:
            print('[ERROR]从diving-fish获取maimaiDX曲目数据超时，正在使用yuzuapi中转获取曲目数据')
            music_data = await mai_api.transfer_music()
            await writefile(music_file, music_data)
        except UnknownError:
            print(
                '[FATAL]从diving-fish获取maimaiDX曲目数据错误。请检查网络环境。\n'
                '[FATAL]请自行使用浏览器访问 "https://www.diving-fish.com/api/maimaidxprober/music_data"'
                '将内容保存为 "music_data.json" 存放在 "static" 目录下并重启此工具'
            )
            raise
        except Exception: # pylint: disable=broad-exception-caught
            print(f'[FATAL]Error: {traceback.format_exc()}')
            print(
                '[FATAL]maimaiDX数据获取错误，请检查网络环境。\n'
                '[FATAL]请自行使用浏览器访问 "https://www.diving-fish.com/api/maimaidxprober/music_data"'
                '将内容保存为 "music_data.json" 存放在 "static" 目录下并重启此工具'
            )
            raise


    total_list: MusicList = MusicList((Music(**music) for music in music_data))

    return total_list

async def music_list_dispatcher(local_first: bool) -> MusicList:
    """Music list dispatcher."""
    return await get_local_music_list() if local_first else await get_music_list()


async def get_user_info(username: str) -> UserInfo:
    """Get user info from diving fish."""
    return UserInfo(**(await mai_api.query_user(username)))
