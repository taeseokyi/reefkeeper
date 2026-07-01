# feedback-regression-test-simulator

> measure_kh_once.py 등 측정/BT 로직 변경은 배포 전 항상 시뮬레이터(bin/test_measure_sim.py)로 회귀 검증

---

measure_kh_once.py(측정·시리얼·RF 순단 로직) 또는 펌웨어 명령 프로토콜을 바꾸면 **배포 전 항상**
WSL 저장소에서 시뮬레이터 회귀 테스트를 돌려 전부 PASS인지 확인한다(사용자 지시 2026-06-23, "기억해").

**How to apply:**
- 실행: `cd bin && python3 test_measure_sim.py` — **WSL 안, 저장소 bin/ 아래**서만(윈도우로 가지 말 것). pyserial 3.5 + `serial.serial_for_url('socket://…')` 사용.
- 전부 PASS여야 `cp bin/measure_kh_once.py /mnt/c/dkh/work/`로 배포.
- 도구 2종(저장소 bin/에만, 윈도우 배포 안 함):
  - `firmware_sim.py` — 소켓 가상 포트 펌웨어 시뮬레이터. 펌웨어 명령 충실 모방, 측정은 상수 pH라 정확히 8회째 평탄 latch, 모터 즉시 완료. 펌웨어 상태가 연결을 가로질러 유지(RF 드롭 모사). 드롭/kill/garble/no_done/hang 예외 주입 가능. 단독 실행 `python3 bin/firmware_sim.py`로 수동 접속 테스트도 됨.
  - `test_measure_sim.py` — **총 12 시나리오 / 58 검증, 전부 PASS여야 함**:
    정상/회복 6(36 검증)=클린 calkh(9)·측정중 드롭after(6)·모터 재시도 정지(5)·calref(5)·측정 in-send 재시도before(5)·calref 드롭(6);
    예외 6(22 검증)=완전두절 kill(3)·깨진응답 pH누락(3)·모터 미완료(3)·버스트 회복(4)·setref 예외(4)·모터정지 명령 드롭(5).

**★배포 안전(중요):** 테스트는 `import measure_kh_once` 후 `mk.MEAS_INTERVAL=0.02`, `mk.FAIL_MAX=2`,
`mk.MEAS_READ_TIMEOUT=0.5`, `mk.LINK_PING_TIMEOUT=0.3` 등으로 **메모리상 모듈만** 패치해 빠르게 돈다.
**소스 파일의 실전 상수는 안 바뀐다**(MEAS_INTERVAL=30·FAIL_MAX=5·MEAS_READ_TIMEOUT=20·
LINK_PING_TIMEOUT=3·RECONNECT_TRIES=5·SEND_RETRY_MAX=3·KEEPALIVE_SECS=12). 그래서 배포본은 정상 동작.
이 분리를 위해 매직넘버를 모듈 상수로 빼 둠(테스트에서 패치 가능하게).

**Why:** RF 순단 대응(연결확인→재연결→재시도→모터정지)·keepalive를 하드웨어 없이 상황별로 검증.
이미 실버그(수신 중 예외 미처리)와 단언 오류를 잡아냄. 관련: [project-measure-kh-script](project-measure-kh-script.md) [project-kh-v4-firmware-state](project-kh-v4-firmware-state.md)
