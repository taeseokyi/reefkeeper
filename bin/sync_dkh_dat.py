#!/usr/bin/env python3
"""Windows 원본 dkh.dat 을 저장소(data/dkh.dat)로 동기화하고 GitHub 에 push한다.

cron으로 주기 실행(예: */20 * * * *). 변경이 없으면 아무것도 커밋하지 않는다
(내용이 같으면 push만 시도 — 이전 실행이 네트워크 문제로 push 실패했을 때 재시도 역할).
그래프(PNG) 렌더링은 여기서 하지 않는다 — push되면 GitHub Actions(plot-dkh.yml)가
data/dkh.dat 변경을 감지해 그린다. 이 스크립트는 순수 동기화만 담당(단일 책임 분리).
"""
import fcntl
import logging
import os
import subprocess
import sys

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/mnt/c/dkh/work/dkh.dat"
DST = os.path.join(REPO_DIR, "data", "dkh.dat")
LOCK_FILE = "/tmp/dkh_sync.lock"
LOG_FILE = os.path.expanduser("~/dkh_sync.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger(__name__)


def run_git(*args):
    return subprocess.run(
        ["git", "-C", REPO_DIR, *args],
        capture_output=True, text=True,
    )


def main():
    if not os.path.exists(SRC):
        log.warning("원본 없음: %s (Windows 드라이브 마운트 확인 필요)", SRC)
        return

    with open(SRC, "rb") as f:
        src_bytes = f.read()

    changed = not os.path.exists(DST) or open(DST, "rb").read() != src_bytes

    if changed:
        os.makedirs(os.path.dirname(DST), exist_ok=True)
        with open(DST, "wb") as f:
            f.write(src_bytes)
        row_count = src_bytes.count(b"\n")
        run_git("add", "data/dkh.dat")
        commit = run_git("commit", "-m", f"data: dkh.dat 동기화 (자동, {row_count}행)")
        if commit.returncode == 0:
            log.info("커밋됨: %s", commit.stdout.strip().splitlines()[0] if commit.stdout else "")
        else:
            log.warning("커밋 실패/변경없음: %s", commit.stderr.strip())

    push = run_git("push")
    if push.returncode == 0:
        if changed:
            log.info("push 완료")
    else:
        log.error("push 실패: %s", push.stderr.strip())


if __name__ == "__main__":
    lock_fd = open(LOCK_FILE, "w")
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        sys.exit(0)  # 이전 실행이 아직 진행 중 — 조용히 종료
    try:
        main()
    except Exception:
        log.exception("동기화 중 예외")
