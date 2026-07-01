# project-windows-files

> Windows 작업 폴더 %USERPROFILE%\Documents\work 파일 현황 및 작업 스케줄러 설정

---

Windows 실행 폴더: `%USERPROFILE%\Documents\work`  
WSL 경로: `/mnt/c/Users/<user>/Documents/work`

**버전 동기화 (2026-06-14):** Windows `measure_kh_once.py`에 대칭화+수렴판정+펌프시간 튜닝 버전 배포 완료(WSL bin/와 동일, 커밋 9b333e2). 펌프시간은 [project-pump-timings](project-pump-timings.md), 시퀀스는 [project-symmetric-kh-redesign](project-symmetric-kh-redesign.md). (`measure_kh_loop.py`는 수동 실행용이라 미배포 — 필요 시 동일 복사.) **dkh.dat은 여전히 Windows가 원본, 절대 덮어쓰지 말 것.**

**파일 목록 (2026-06-10 기준):**
- `dkh_server.py` — KH JSON API 서버
- `measure_kh_loop.py` — 정시 반복 측정 (수동 실행용)
- `measure_kh_once.py` — 1회 측정 (스케줄러 호출용)
- `test_pump.py` — 펌프 시험
- `dkh.dat` — 실측 데이터 (Windows가 원본, WSL 버전과 내용 다름)
- `start_dkh_server.bat` — dkh_server.py 실행용 배치
- `register_task.bat` / `register_task.ps1` — DKH Server 스케줄러 등록
- `register_measure_kh.bat` / `register_measure_kh.ps1` — Measure KH 스케줄러 등록

**ASCII junction 폴더 `C:\dkh\` (한글 경로 우회용, 2026-06-10 신설):**
- `C:\dkh\work` → `%USERPROFILE%\Documents\work` (junction)
- `C:\dkh\python313` → `%LOCALAPPDATA%\Programs\Python\Python313` (junction)
- `C:\dkh\dkh_server.log` — dkh_server.py가 직접 기록 (Windows에서 `logging filename`으로 파일 로깅)
- `C:\dkh\fix_junctions.ps1` — junction 재생성 (env 변수 사용, 한글 리터럴 없음)
- junction은 WSL `/mnt/c`에서 따라가지 못함 → 검증은 `powershell Test-Path`로.

**Windows 작업 스케줄러 (`\tsyi\` 폴더, 총 4개):**
| 작업명 | 트리거 | 동작 |
|--------|--------|------|
| DKH Server | **로그인 시(AtLogOn)** | `C:\dkh\python313\pythonw.exe C:\dkh\work\dkh_server.py` 직접 실행 (cmd/bat 없음) |
| Measure KH | 매일 05:00 / 13:00 / 21:00 (8h 간격 3회, 반복패턴 없음) | `pythonw C:\dkh\work\measure_kh_once.py` (COM15, 블루투스라 연결마다 변동), 출력→`C:\dkh\measure_kh.log` |
| `불루투스-10 시간 설정` (오타 주의: 불루투스) | 매일 05:20 | `pythonw set_time.py COM10` 시계동기 |
| `블루투스 시간 설정` | 매일 05:40 | `pythonw set_time.py COM12` 시계동기 |

**블루투스 시계동기 작업 2개 (2026-06-10 AHK→pyserial 전환):**
- **컨트롤러 실제 포트: COM10, COM12** (measure_kh의 포트와 별개 → 시리얼 충돌 없음). **블루투스 COM 포트는 페어링에 묶임 — 한 번 연결되면 유지되고, 장치 삭제 후 재연결할 때만 번호가 바뀜**(매 연결마다 X) → 재페어링 후엔 실제 할당 포트 확인 필수. 옛 AHK 인자 9/10은 COM번호가 아니라 아두이노IDE Tools>Port 메뉴 위치였음(혼동 주의).
- **현재 방식: `bin/set_time.py` (pyserial 직접 전송).** 인자로 포트(`COM10`/`COM12` 또는 숫자) + 선택적 baud. 9600, 연결 후 2초 대기 + reset_input_buffer, **전송 직전 시각 캡처** 후 `set time HH:MM:SS` 전송, 응답을 `C:\dkh\set_time.log`(UTF-8)에 기록. pythonw로 실행(콘솔 없음). 작업 `ExecutionTimeLimit=PT2M`(장치 꺼짐 시 시리얼 open hang 방지).
- **펌웨어 핵심 특성(COM10/COM12):** ①**줄바꿈은 LF(`\n`)만** — `\r` 붙으면 명령 미실행, echo만 함(measure_kh의 COM15는 `\r\n` 사용 — 펌웨어 다름!). ②**모든 입력을 echo**: `수신 명령문 : <명령>` 출력 → 전달 검증용. ③인코딩 UTF-8. ④`help` 명령 목록: `help, debug, refresh all, debug reset, time, set time hh:mm:ss, reset, ltest ssss, rtest ssss, ls, lrt ssss, lgt mmm, rrt ssss, rgt mmm, off, on`. ⑤`time`으로 현재 시각 조회 가능(`Current time : HH:MM:SS.mmm`).
- 옛 자료: `%USERPROFILE%\Desktop\sketch_may08a\` (`adu-srial-port.ahk`/`.exe`/`.lnk`/`.xml`) — 더 이상 안 씀(IDE GUI 자동화, 취약). 임시 진단 스크립트 `C:\dkh\probe.py`,`probe_raw.py`,`*.bin`은 정리 가능.
- 배터리/유휴: 4개 작업 모두 `DisallowStartIfOnBatteries=False, StopIfGoingOnBatteries=False, IdleStop=False`. 전환 스크립트 `C:\dkh\update_bluetooth_tasks.ps1`(액션 exe경로로 대상식별, 한글 리터럴 0개, 관리자 실행).

**DKH Server 작업 핵심 설정 (반드시 유지):**
- `DisallowStartIfOnBatteries=False`, `StopIfGoingOnBatteries=False`, `IdleSettings.StopOnIdleEnd=False`, `ExecutionTimeLimit=PT0S`
- **이게 진짜였던 버그:** 기본값(배터리/유휴 시 작업 중지)이 데몬을 로그 없이 hard-terminate → 부팅 후 2분 만에 죽음. 노트북이라 발생.
- 데몬이므로 작업 상태는 항상 `Running`(LastTaskResult 267009=0x41301)이 정상.
- `register_task.ps1`은 한글 리터럴 0개(전부 `$env:`) + junction 재생성 포함. 등록은 관리자 PowerShell 필요.
- `pythonw.exe` 사용 이유: 콘솔창 없음 + cmd/자식프로세스 정리 문제 회피. `start_dkh_server.bat`는 더 이상 안 씀(obsolete).
- WSL `schtasks /Run`은 "트리거 시도" 메시지가 떠도 실제 실행됨 — port/log로 확인.

**Measure KH 트리거 방식 (2026-06-14 변경):** Daily 트리거 3개(05:00/13:00/21:00), 반복패턴(Repetition) 없음 → 하루 3회 8시간 간격. `register_measure_kh.ps1`의 `$trigger`가 3개 `New-ScheduledTaskTrigger -Daily -At` 배열. (이전: Daily 00:00 + PT1H/P1D 매시간.) 재등록은 관리자 권한 필요 → WSL에서 `Start-Process powershell -Verb RunAs`로 UAC 승격 실행.
**Measure KH (2026-06-10 통일):** 배터리/유휴 OFF, `ExecutionTimeLimit=PT5H`(★2026-06-22 확인 — 옛 PT55M 아님. 스크립트 내부 상한 ~4h에 1h 여유 둔 바깥 안전망). `python`→`pythonw`(콘솔창 제거) + junction 경로(`C:\dkh\python313\pythonw.exe C:\dkh\work\measure_kh_once.py`). measure_kh_once.py에 `setup_logging()` 추가: pythonw는 `sys.stdout=None`이라 print가 죽으므로 stdout/stderr를 `C:\dkh\measure_kh.log`로 redirect(줄단위 flush, 1MB 초과 시 새로시작, 실패 시 devnull). `register_measure_kh.ps1`은 한글 리터럴 없음.

**실행 조건 / 재부팅·로그인 동작 (2026-06-10 확정):**
- 두 작업 모두 **로그인된 대화형 세션에서만 동작.** Measure KH는 `LogonType=InteractiveToken`(현재 로그인 사용자 토큰으로 실행), DKH Server는 트리거가 `AtLogOn`. 로그인 전(잠금/로그온 화면)에는 둘 다 안 돎.
- **로그아웃하면 둘 다 죽음**(세션·토큰 파괴 → pythonw 종료, AtLogOn은 다음 로그인까지 재기동 안 함). **잠금(Win+L)은 세션 유지되어 계속 동작** → 자리 비울 땐 로그아웃 말고 잠금. 절전/디스플레이off는 OK(배터리·유휴 정지 이미 해제됨).
- 왜 로그인 필요: COM15/COM10/COM12 등 **시리얼·블루투스 COM 포트가 사용자 세션에 바인딩**되어 session 0(비대화형, "로그온 여부와 무관 실행")에서는 접근/열거 불가 위험 → 의도된 설계. 자동 복귀 원하면 **자동 로그인(autologon)** 권장.
- Measure KH 트리거는 **고정 시각**(매일 05:00/13:00/21:00, 매일 재무장) → 재부팅해도 스케줄 안 깨지고 부팅·로그인 후 다음 예정 시각부터 정상 재개. `StartWhenAvailable` 미설정이라 **꺼져 있던 시간대 측정은 보충 안 함**(의도, [feedback-no-catchup-measure](feedback-no-catchup-measure.md)).
- `MultipleInstancesPolicy=IgnoreNew` → 직전 측정(최대 55분)이 진행 중이면 다음 정시 트리거는 **스킵**. 부팅 직후 등 충돌 시 1회 스킵 가능(LastTaskResult 0x80070002 등)하나 다음 정시는 정상.
- **측정 1회 상한 시간(2026-06-22 확인):** 스크립트 내부=phase(tank/ref)별 `PHASE_MAX_SECS=7200초(2h)`·`MEAS_MAX=240회` → 2-phase라 **최대 ~4h**(미평탄/행 상황 상한, 초과 시 마지막값+경고로 종료, 무한대기 방지). 바깥 스케줄러 `ExecutionTimeLimit=PT5H`가 5h에서 강제종료(1h 여유). 정상 평탄 도달이 빠르면 보통 수십 분 내 종료, 4h/5h는 어디까지나 상한. (상수 변경 이력은 [project-kh-v4-firmware-state](project-kh-v4-firmware-state.md): 6/21 PHASE_MAX 2400→7200, MEAS_MAX 80→240.) `dkh.dat`는 **완료 시점에만** 기록 → 측정 중 dkh.dat·API가 직전값 그대로인 건 정상. 작업 LastTaskResult `267009`(0x41301)=실행 중, `0`=정상 완료.

**Why:** 부팅 후 자동 서버 기동 및 매시간 KH 자동 측정.
**How to apply:** `dkh.dat`는 Windows 원본을 절대 WSL 버전으로 덮어쓰지 않는다. bin/ 변경 시 Windows 폴더에도 복사 필요 (dkh.dat 제외).
