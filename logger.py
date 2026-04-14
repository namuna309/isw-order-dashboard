from __future__ import annotations

import logging
from pathlib import Path


LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "app.log"


def setup_logger() -> logging.Logger:
    LOG_DIR.mkdir(exist_ok=True)

    logger = logging.getLogger("ilshin_bot")

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def cleanup_log_file(
    logger: logging.Logger,
    max_size_mb: int = 5
) -> None:
    """
    로그 파일이 max_size_mb 초과 시 초기화
    """
    try:
        if not LOG_FILE.exists():
            return

        file_size = LOG_FILE.stat().st_size
        file_size_mb = file_size / (1024 * 1024)

        logger.info(
            f"로그 파일 크기 확인: {file_size_mb:.2f} MB"
        )

        if file_size_mb > max_size_mb:
            logger.info(
                f"로그 파일이 {max_size_mb}MB 초과 "
                "→ 로그 초기화"
            )

            # 파일 비우기
            LOG_FILE.write_text(
                "",
                encoding="utf-8"
            )

            logger.info("로그 파일 초기화 완료")

    except Exception as exc:
        logger.warning(
            f"로그 파일 정리 중 오류 발생: {exc}"
        )