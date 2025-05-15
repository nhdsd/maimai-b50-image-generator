"""
User Data Parser
"""

from typing import cast, Dict, Any

from .models import UserInfo
from .api import mai_api
from .consts import root
from .tools import openfile

async def get_user_data(
        source: str,
        username: str
    ) -> UserInfo:
    """Get user data from given source."""
    match source:
        case "diving_fish":
            return UserInfo(**(await mai_api.query_user(username)))
        case "diving_fish_local":
            return UserInfo(**cast(Dict[str, Any], await openfile(root / 'data.json')))
        case _:
            raise ValueError("[FATAL]无效的数据源。")
