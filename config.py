from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    target_url: str
    user_id: str
    user_pw: str
    chrome_user_data_dir: str
    chrome_profile_directory: str
    window_title_regex: str
    id_box_x: int
    id_box_y: int
    load_wait_seconds: int
    post_login_wait_seconds: int


def _require_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise ValueError(f"{name} 환경변수가 비어 있습니다.")
    return value


def load_settings() -> Settings:
    return Settings(
        target_url=_require_env("TARGET_URL"),
        user_id=_require_env("ISW_USER_ID"),
        user_pw=_require_env("ISW_USER_PW"),
        chrome_user_data_dir=_require_env("CHROME_USER_DATA_DIR"),
        chrome_profile_directory=_require_env("CHROME_PROFILE_DIRECTORY"),
        window_title_regex=_require_env("WINDOW_TITLE_REGEX"),
        id_box_x=int(_require_env("ID_BOX_X")),
        id_box_y=int(_require_env("ID_BOX_Y")),
        load_wait_seconds=int(os.getenv("LOAD_WAIT_SECONDS", "5")),
        post_login_wait_seconds=int(os.getenv("POST_LOGIN_WAIT_SECONDS", "10")),
    )