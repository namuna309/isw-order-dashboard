from __future__ import annotations

import sys

from config import load_settings
from login import login
from logger import setup_logger

logger = setup_logger()


def main() -> int:
    try:
        logger.info("프로그램 시작")

        settings = load_settings()

        logger.info("환경변수 로딩 완료")

        driver = login(settings)

        logger.info("로그인 시도 완료")
        logger.info(f"현재 URL: {driver.current_url}")

        return 0

    except Exception as exc:
        logger.exception(f"오류 발생: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())