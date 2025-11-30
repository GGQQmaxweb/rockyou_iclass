# schools/config.py
from dataclasses import dataclass
from typing import Callable, Optional, Union, Awaitable
import logging
import requests
from schools.http_headers import session_headers

from schools.http_headers import session_headers  # 或你實際使用的 Session 類型

logger = logging.getLogger(__name__)

Session = requests.Session  # 視你實際用的型別而定


@dataclass(frozen=True)
class SchoolConfig:
    key: str  # "tku", "fju", ...
    auth_func: Callable[
        [], Awaitable[Union[Session, dict]]
    ]  # 不吃參數，回傳已登入的 session 或錯誤 dict
    endpoint: Optional[str] = None  # 有些學校可能不需要 endpoint（只登入）
    latitude: float = 25.174269373936202  # default latitude
    longitude: float = 121.45422774303604  # default longitude


async def tku_auth() -> Union[Session, dict]:
    from schools.tku.auth import Authenticator

    logger.info("🔐 Logging in (TKU)...")
    auth = await Authenticator.create()
    session = auth.perform_auth()

    # Check if authentication failed
    if isinstance(session, dict) and "error" in session:
        logger.error("TKU authentication failed: %s", session["error"])
        return session

    session.headers.update(session_headers())
    logger.info("TKU session initialized.")
    return session


async def fju_auth() -> Session:
    from schools.fju.auth import Authenticator

    logger.info("🔐 Logging in (FJU)...")
    auth = await Authenticator.create()
    session = auth.login()
    session.headers.update(session_headers())
    logger.info("FJU session initialized.")
    return session


async def au_auth() -> Union[Session, dict]:
    from schools.au.auth import Authenticator

    auth = await Authenticator.create()
    session = auth.login()
    session.headers.update(session_headers())
    logger.info("AU session initialized.")
    return session


SCHOOL_CONFIGS: dict[str, SchoolConfig] = {
    "tku": SchoolConfig(
        key="tku",
        auth_func=tku_auth,
        endpoint="https://iclass.tku.edu.tw",
        latitude=25.174269373936202,
        longitude=121.45422774303604,
    ),
    "fju": SchoolConfig(
        key="fju",
        auth_func=fju_auth,
        endpoint="https://elearn2.fju.edu.tw",
        latitude=25.03659879562293,
        longitude=121.4328216507679,
    ),
    "au": SchoolConfig(
        key="au",
        auth_func=au_auth,
        endpoint="https://tronclass.asia.edu.tw",
        latitude=24.968099,
        longitude=121.19054,
    ),
    # 未來要 100 間學校，就在這裡繼續加：
    # "abc": SchoolConfig(key="abc", auth_func=abc_auth, endpoint="https://..."),
}
