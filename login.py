from __future__ import annotations

import time

from pywinauto import Desktop
from pywinauto.keyboard import send_keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from config import Settings


def build_driver(settings: Settings) -> webdriver.Chrome:
    """
    webdriver-manager를 사용해 현재 Chrome 버전에 맞는 드라이버 자동 설치
    """
    options = Options()

    # 기존 크롬 프로필 재사용 (ShiftCrossBrowser 확장 포함)
    options.add_argument(f"--user-data-dir={settings.chrome_user_data_dir}")
    options.add_argument(f"--profile-directory={settings.chrome_profile_directory}")

    options.add_argument("--start-maximized")

    # webdriver-manager 자동 다운로드
    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=options)
    return driver


def open_target_page(driver: webdriver.Chrome, settings: Settings) -> None:
    driver.get(settings.target_url)
    time.sleep(settings.load_wait_seconds)


def find_target_window(settings: Settings):
    """
    ShiftCrossBrowser / 대리점 로그인 창 찾기
    """
    window = Desktop(backend="uia").window(
        title_re=settings.window_title_regex
    )
    window.wait("visible", timeout=20)
    window.set_focus()
    return window


def click_id_box(window, settings: Settings) -> None:
    """
    ID 입력칸 클릭
    coords는 창 내부 상대좌표 기준
    """
    window.click_input(coords=(settings.id_box_x, settings.id_box_y))
    time.sleep(0.5)


def input_credentials(settings: Settings) -> None:
    """
    아이디 / 비밀번호 입력 후 로그인
    """
    send_keys("^a{BACKSPACE}")
    send_keys(settings.user_id, with_spaces=True)

    send_keys("{TAB}")

    send_keys("^a{BACKSPACE}")
    send_keys(settings.user_pw, with_spaces=True)

    send_keys("{ENTER}")


def login(settings: Settings) -> webdriver.Chrome:
    """
    전체 로그인 플로우
    """
    driver = build_driver(settings)

    open_target_page(driver, settings)

    window = find_target_window(settings)

    click_id_box(window, settings)

    input_credentials(settings)

    time.sleep(settings.post_login_wait_seconds)

    return driver