from __future__ import annotations

import sys

from config import load_settings
from login import login
from logger import (
    setup_logger,
    cleanup_log_file,
)

logger = setup_logger()


def main() -> int:
    exit_code = 0

    try:
        logger.info("프로그램 시작")

        settings = load_settings()

        logger.info("환경변수 로딩 완료")

        driver = login(settings)

        logger.info("로그인 시도 완료")
        # logger.info(f"현재 URL: {driver.current_url}")

    except Exception as exc:
        logger.exception(f"오류 발생: {exc}")
        exit_code = 1

    finally:
        cleanup_log_file(
            logger=logger,
            max_size_mb=5
        )

    return exit_code


if __name__ == "__main__":
    sys.exit(main())