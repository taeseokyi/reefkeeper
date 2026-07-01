# feedback-run-windows-py-from-wsl

> WSL에서 Windows Python 스크립트(test_pump 등) 실행하는 정해진 방법 (-X utf8 필수)

---

"윈도우에서 (test_pump 등) 실행해줘"라고 하면 WSL에서 Windows Python으로 직접 돌린다. 정해진 명령:

```bash
/mnt/c/dkh/python313/python.exe -X utf8 'C:\dkh\work\test_pump.py' 2>&1
```

- **`python.exe`** 사용(콘솔 출력 봐야 하므로 `pythonw` 아님). 경로는 ASCII junction(`C:\dkh\python313`, `C:\dkh\work`) 사용 — 한글 경로 우회. [project-windows-files](project-windows-files.md)
- **`-X utf8` 플래그 필수.** Windows 콘솔 기본 인코딩이 cp949라 스크립트의 `—`(—) 같은 유니코드 문자에서 `UnicodeEncodeError`로 죽는다. `PYTHONIOENCODING=utf-8`/`PYTHONUTF8=1` 환경변수는 WSL→Windows 프로세스로 전달이 안 됨(WSLENV 미설정) → 안 통하므로 반드시 `-X utf8` 명령행 플래그를 쓴다.
- 펌프 시험은 모터 동작+측정이라 수 분 걸림 → Bash timeout 넉넉히(300000ms).
- 측정 포트(현재 COM15)는 Measure KH 스케줄러와 공유 → 예정 측정(05/13/21시) 중이면 시리얼 충돌, SerialException으로 끝나면 재시도. 포트 번호는 블루투스 재페어링 시 바뀜([project-measure-kh-script](project-measure-kh-script.md) 참고).

**Why:** 매번 인코딩 오류로 두세 번 헛돌았음. 정해진 형태로 한 번에 실행하기 위함.
**How to apply:** 같은 패턴을 measure_kh_once.py 등 다른 Windows 스크립트 수동 실행에도 적용.
