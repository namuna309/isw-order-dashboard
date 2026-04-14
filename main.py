from __future__ import annotations

import sys

from config import load_settings
from login import login


def main() -> int:
    try:
        settings = load_settings()

        driver = login(settings)

        print("로그인 시도 완료")
        print("현재 URL:", driver.current_url)

        return 0

    except Exception as exc:
        print(f"오류 발생: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())