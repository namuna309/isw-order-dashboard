from __future__ import annotations

import time

from pywinauto import Desktop
from pywinauto.keyboard import send_keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from config import Settings
from logger import setup_logger

logger = setup_logger()


def build_driver(settings: Settings) -> webdriver.Chrome:
    logger.info("ChromeDriver 초기화 시작")

    options = Options()

    if settings.chrome_user_data_dir:
        logger.info(f"Chrome user data dir 사용: {settings.chrome_user_data_dir}")
        options.add_argument(
            f"--user-data-dir={settings.chrome_user_data_dir}"
        )

    if settings.chrome_profile_directory:
        logger.info(
            f"Chrome profile 사용: {settings.chrome_profile_directory}"
        )
        options.add_argument(
            f"--profile-directory={settings.chrome_profile_directory}"
        )

    options.add_argument("--start-maximized")

    logger.info("ChromeDriver 다운로드 및 실행 중...")
    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=options)

    logger.info("ChromeDriver 실행 완료")

    return driver


def open_target_page(driver: webdriver.Chrome, settings: Settings) -> None:
    logger.info(f"사이트 접속 시작: {settings.target_url}")

    driver.get(settings.target_url)

    logger.info(
        f"{settings.load_wait_seconds}초 대기 (페이지 로딩 대기)"
    )
    time.sleep(settings.load_wait_seconds)

    logger.info(f"현재 URL: {driver.current_url}")


def find_target_window(settings: Settings):
    logger.info(
        f"대상 창 탐색 시작 (정규식: {settings.window_title_regex})"
    )

    desktop = Desktop(backend="uia")

    windows = desktop.windows(
        title_re=settings.window_title_regex,
        top_level_only=True
    )

    visible_windows = []

    for idx, win in enumerate(windows):
        try:
            title = win.window_text()
            is_visible = win.is_visible()

            logger.info(
                f"[후보 창 {idx}] title={title!r}, visible={is_visible}"
            )

            if is_visible:
                visible_windows.append(win)

        except Exception as exc:
            logger.warning(
                f"[후보 창 {idx}] 조회 실패: {exc}"
            )

    if not visible_windows:
        raise RuntimeError(
            "제목에 '대리점'이 포함된 visible 창을 찾지 못했습니다."
        )

    # 마지막 visible 창 사용
    window = visible_windows[-1]

    logger.info(
        f"선택된 창 제목: {window.window_text()!r}"
    )

    window.set_focus()

    time.sleep(0.5)

    logger.info("창 포커스 완료")

    return window

def input_credentials(settings: Settings) -> None:

    logger.info("비밀번호 입력 시작")

    send_keys("^a{BACKSPACE}")
    send_keys(settings.user_pw, with_spaces=True)

    logger.info("비밀번호 입력 완료")

    logger.info("로그인 엔터 입력")

    send_keys("{ENTER}")

    logger.info("로그인 요청 완료")


def login(settings: Settings) -> webdriver.Chrome:
    logger.info("=== 로그인 프로세스 시작 ===")

    driver = build_driver(settings)

    open_target_page(driver, settings)

    window = find_target_window(settings)

    input_credentials(settings)

    logger.info(
        f"{settings.post_login_wait_seconds}초 대기 "
        "(로그인 후 화면 전환 대기)"
    )

    time.sleep(settings.post_login_wait_seconds)

    logger.info("=== 로그인 프로세스 종료 ===")

    return driver